import sqlite3
from flask import Flask, request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from src.models import db, Log, User, update_dog, ShelterDogs

app = Flask(__name__)

app.config['SECRET_KEY'] = 'securekey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from sqlalchemy.sql.functions import current_user

@app.before_request
def before_request():
    # token = request.headers.get('x-access-token')
    # user = User.query.filter_by(latesttoken=token).first()
    now = datetime.datetime.utcnow()

    new_log = Log(user=current_user.name, endpoint=request.endpoint, timestamp=now)
    from app import db
    db.session.add(new_log)
    db.session.commit()
    print(f'Accessed API {request.endpoint} \t {now.strftime("%Y-%m-%d %H:%M:%S")}')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'No token.'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET-KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': "Can't perform that function"})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': "Can't perform that function"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': "Can't perform that function"})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    print("User created")
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': "Can't perform that function"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': "Can't perform that function"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate', 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate', 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
            app.config['SECRET_KEY'])

        # user.latesttoken = token
        # db.session.commit()
        return jsonify({'token': token.encode().decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate', 'Basic realm="Login required!"'})


def create_app():
    app = Flask(__name__)

    # Register the open blueprint with app object
    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    # Register the user blueprint with app object
    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    # Register the admin blueprint with app object
    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    return app


@app.route("/dog/create", methods=['POST'])
def createdog():
    sqliteconnection = sqlite3.connect('db.sqlite')
    cursor = sqliteconnection.cursor()

    cursor.execute('SELECT ID FROM shelter_dogs WHERE ID IN ( SELECT max( ID ) FROM shelter_dogs );')
    row = cursor.fetchone()
    rownumb = row[0] + 1

    dogdata = request.get_json()

    new_dog = ShelterDogs(ID=rownumb, name=dogdata["name"], age=dogdata["age"], sex=dogdata["sex"],
                          breed=dogdata["breed"], color=dogdata["color"], coat=dogdata["coat"],
                          size=dogdata["size"],
                          neutered=dogdata["neutered"], likes_children=dogdata["likes_children"])
    db.session.add(new_dog)
    db.session.commit()

    return jsonify({'message: New dog created with the index:': rownumb})


@app.route("/dog/read", methods=["GET"])
def readdog():
    dogs = ShelterDogs.query.all()

    output = []

    for filtdog in dogs:
        dogs_data = {'ID': filtdog.ID, 'name': filtdog.name, 'age': filtdog.age,
                     'breed': filtdog.breed}
        output.append(dogs_data)
    return jsonify({'dogs': output})


@app.route("/dog/read/<name>", methods=["PUT"])
def readsomedogs(name):
    try:
        sqliteconnection = sqlite3.connect('db.sqlite')
        cursor = sqliteconnection.cursor()

        sql_select_query = """select * from shelter_dogs where name = ?"""
        cursor.execute(sql_select_query, (name,))
        records = cursor.fetchall()
        output = []
        for row in records:
            dogsearch = f'index: {row[0]}, name: {row[1]}, age: {row[2]}, sex: {row[3]}, breed: {row[4]},' \
                        f' color: {row[5]}, coat: {row[6]}, size: {row[7]}, neutered: {row[8]}, likes_children: {row[9]}'
            output.append(dogsearch)

        return jsonify({'You searched for': name}, {"Here are the results": output})
        cursor.close()

    except sqlite3.Error as error:
        return jsonify("Failed to read data", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


@app.route("/dog/update", methods=["PUT"])
def updatedog():
    request_data = request.get_json()
    update_dog(request_data['ID'], request_data['name'], request_data['age'], request_data["sex"],
               request_data['breed'],
               request_data['color'], request_data['coat'], request_data['size'], request_data['neutered'],
               request_data['likes_children'])
    response = Response("Dog Updated", status=200, mimetype='application/json')
    return response


@app.route("/dog/delete/<id>", methods=["DELETE"])
def deletedog(id):
    try:
        sqliteconnection = sqlite3.connect('db.sqlite')
        cursor = sqliteconnection.cursor()
        sql_select_query = """select * from shelter_dogs where ID = ?"""
        cursor.execute(sql_select_query, (id,))
        records = cursor.fetchall()
        output = []
        for row in records:
            dogsearch = f'index: {row[0]}, name: {row[1]}, age: {row[2]}, sex: {row[3]}, breed: {row[4]},' \
                        f' color: {row[5]}, coat: {row[6]}, size: {row[7]}, neutered: {row[8]}, likes_children: {row[9]}'
            output.append(dogsearch)
        sql_delete_query = """DELETE from shelter_dogs where ID = ?"""
        cursor.execute(sql_delete_query, (id,))
        sqliteconnection.commit()
        cursor.close()
        return jsonify({"You have chosen to delete": output}, "Dog deleted successfully")

    except sqlite3.Error as error:
        return jsonify("Failed to read data", error)
    finally:
        if sqliteconnection:
            sqliteconnection.close()


@app.errorhandler(500)
def internal_error(error):
    return "500 error - Internal Server Exception \n Did you write everything correctly?", 500


if __name__ == "__main__":
    app = create_app()
    app.run()

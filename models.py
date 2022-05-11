import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    #latesttoken = db.Column(db.String)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    endpoint = db.Column(db.String)
    user = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


def update_dog(_ID, _name, _age, _sex, _breed, _color, _coat, _size, _neutered, _likes_children):
    dog_to_update = ShelterDogs.query.filter_by(ID=_ID).first()
    dog_to_update.name = _name
    dog_to_update.age = _age
    dog_to_update.sex = _sex
    dog_to_update.breed = _breed
    dog_to_update.color = _color
    dog_to_update.coat = _coat
    dog_to_update.size = _size
    dog_to_update.neutered = _neutered
    dog_to_update.likes_children = _likes_children
    db.session.commit()


class ShelterDogs(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    sex = db.Column(db.String)
    breed = db.Column(db.String)
    color = db.Column(db.String)
    coat = db.Column(db.String)
    size = db.Column(db.String)
    neutered = db.Column(db.String)
    likes_children = db.Column(db.String)

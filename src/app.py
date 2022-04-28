from flask import Flask



def create_app():
    app = Flask(__name__)

    # Register the open blueprint with app object
    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    # Register the open blueprint with app object
    from blueprints.user import bp_user
    app.register_blueprint(bp_user)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
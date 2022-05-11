from flask import Flask


def create_flaskapp():
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

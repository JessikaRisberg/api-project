import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    latesttoken = db.Column(db.String)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    endpoint = db.Column(db.String)
    user = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

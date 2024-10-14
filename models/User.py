import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    # coins = db.Column(db.Integer, deafault=0)

class Categoties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     task_name = db.Column(db.String, nullable=False)
#     description = db.Column(db.String)
#     coast = db.Column(db.Integer, nullable=False) # стоимость покупки
#     compensation = db.Column(db.Integer) # вознаграждение за выполнение
#     data_create = db.Column(db.DateTime, default=datetime.datetime.now())
#     status = db.Column(db.String) # completed, awaiting_review, in_hand, vacant








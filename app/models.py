import datetime

from sqlalchemy import DateTime, String, Integer

from app.app import db


class Employees(db.Model):
    __tablename__ = 'list_of_employees'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(String)
    name = db.Column(String)
    patronymic = db.Column(String)
    position = db.Column(String)
    start_work_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    salary = db.Column(String)
    boss = db.Column(String)
    def __init__(self, surname, name, patronymic, position):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.position = position

    def __repr__(self):
        return f'{self.__class__}, surname: {self.surname}, name: {self.name}, patronymic: {self.patronymic}, position: {self.position}'
class Bosses(db.Model):
    __tablename__ = 'bosses_table'
    id = db.Column(Integer, primary_key=True)
    employer_id = db.Column(Integer)
    surname = db.Column(String)
    name = db.Column(String)
    patronymic = db.Column(String)

import datetime

from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import relationship, backref

from app.app import db


class Employees(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(String)
    name = db.Column(String)
    patronymic = db.Column(String)
    position = db.Column(String)
    start_work_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    salary = db.Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f'{self.__class__}, surname: {self.surname}, name: {self.name}, patronymic: {self.patronymic}, position: {self.position}'


class SubordinationLinks(db.Model):
    __tablename__ = 'subordination_links'
    boss_id = db.Column(Integer, db.ForeignKey('employees.id'), primary_key=True)
    employer_id = db.Column(Integer, db.ForeignKey('employees.id'), primary_key=True)

    boss = relationship(Employees, foreign_keys=[boss_id], backref=backref("subordinates", cascade="all,delete"))
    subordinate = relationship(Employees, foreign_keys=[employer_id], backref=backref("bosses", cascade="all,delete"))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
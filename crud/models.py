from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, UniqueConstraint, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main import app
url = "postgresql://user:123456@188.243.57.73:29650/tree_base"
app.config['SQLALCHEMY_DATABASE_URI'] = url

db = SQLAlchemy(app)
Base = declarative_base()

class Employees(db.Model):
    __tablename__ ='list_of_employees'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    name = db.Column(db.String)
    patronymic = db.Column(db.String)
    position = db.Column(db.String)
    start_work_date = db.Column(db.String)
    salary = db.Column(db.String)
    boss = db.Column(db.String)

class Bosses(db.Model):
    __tablename__ = 'bosses_table'
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer)
    surname = db.Column(db.String)
    name = db.Column(db.String)
    patronymic = db.Column(db.String)



engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

# Создание всех таблиц
Base.metadata.create_all(engine)




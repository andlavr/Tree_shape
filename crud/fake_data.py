import itertools
import random

import requests
from faker import Faker

from app.app import app
from app.models import Employees
from app.models import db

fake = Faker('ru_RU')


def create_employer():
    """
    Создает фейкового работника
    :return: dict
    """
    fullname = fake.name()
    return {
        "surname": fullname.split()[0],
        "name": fullname.split()[1],
        "patronymic": fullname.split()[2],
        "position": fake.job(),
        "start_work_date": fake.date(),
        "salary": random.randint(10000, 100000),
    }


def create_employers():
    """
    Создает 5 списков по 10 000 работников
    :return: None
    """
    for _ in range(5):
        users = []
        for _ in range(10000):
            fullname = fake.name()
            users.append({
                "surname": fullname.split()[0],
                "name": fullname.split()[1],
                "patronymic": fullname.split()[2],
                "position": fake.job(),
                "start_work_date": fake.date(),
                "salary": random.randint(10000, 100000),
            })

            users_data = {"users": users}

        res = requests.post('http://localhost:5000/employees', json=users_data)
        print(res.text)


def create_bosses():
    """
    Выводит id всех работников
    :return: list
    """
    with app.app_context() as context:
        ids = db.session.query(Employees.id).all()
        ids = [i[0] for i in ids]
        print(ids)

        # print(list(zip(ids, reversed(ids))))

        # ids_random = itertools.combinations(ids, 5)
        # for elem in ids_random:
        #     print(elem)
        # two_ids = random.choices(ids, k=2)
        # two_ids = [i[0] for i in two_ids]

        # res = requests.post('http://localhost:5000/bosses', json={"ids": two_ids})


if __name__ == '__main__':
    # create_employers()
    create_bosses()

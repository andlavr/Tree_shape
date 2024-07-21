from flask import request

from app.app import app, db
from app.models import Employees, Bosses

from crud.bosses import two_ids


# @app.route('/')
# def main():
#     return {'Test':'test'}

@app.route('/', methods=['GET'])
def index():
    return {'message': 'Hello!'}


@app.route('/employer', methods=['POST'])
def add_employer():
    """
    Добавляет работника в БД
    @return:
    """


    if request.method == 'POST':
        data = request.get_json()["user"]
        print(data)

        new_employee = Employees(
            surname=data['surname'],
            name=data['name'],
            patronymic=data['patronymic'],
            salary=data['salary'],
            position=data['position'],
            start_work_date=data['start_work_date']
        )
        db.session.add(new_employee)
        db.session.commit()
        db.session.refresh(new_employee)
        return {'message': f'Employees {new_employee.id}, was added to database', 'id': new_employee.id}


@app.route('/employees', methods=['POST'])
def add_employees():
    if request.method == 'POST':
        print('Add new employee')
        data = request.get_json()["users"]
        print(data)
        # users = []
        for elem in data:
            print(elem)

            new_employee = Employees(
                surname=elem['surname'],
                name=elem['name'],
                patronymic=elem['patronymic'],
                salary=elem['salary'],
                position=elem['position'],
                start_work_date=elem['start_work_date']
            )
            db.session.add(new_employee)
        db.session.commit()
        db.session.refresh(new_employee)
        return {'message': f'Employees {new_employee.id}, was added to database'}


@app.route('/bosses/', methods=['POST'])
def add_bosses_employees_ids():
    """
    Добавляет id басса с id работника
    :return:
    """
    if request.method == 'POST':
        data = request.get_json()["ids"]
        b = Bosses(id=data[0], employer_id=data[1])
        db.session.add(b)
        db.session.commit()
        return {'message': f'{data[0]} and {data[1]} was added to database'}


if __name__ == '__main__':
    app.run(debug=True)

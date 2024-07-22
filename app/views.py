import json
import traceback

from flask import request, jsonify, render_template

from app import crud
from app.app import app


@app.route('/', methods=['GET'])
def index():
    return {'message': 'Hello!'}


@app.route('/employer', methods=['POST'])
def add_employer():
    """
    Добавление работника в БД

    :return:
    """

    if request.method == 'POST':
        data = request.get_json()["user"]

        employer = crud.add_employer(data)

        return {'message': f'Employees {employer.id}, was added to database', 'id': employer.id}


@app.route('/subordination_links/', methods=['POST'])
def add_subordination_links():
    """
    Связывает id босса и id работника

    :return:
    """

    if request.method == 'POST':
        data = request.get_json()["ids"]

        if crud.add_subordination_links(data):
            return {'message': f'{data[0]} and {data[1]} was added to database'}
        return {'message': f"{data[0]} and {data[1]} not added to database"}


@app.route('/fill_db', methods=['POST'])
def fill_db():
    """
    Добавляет все дерево в БД
    :return:
    """

    if request.method == 'POST':
        data = request.get_json()['tree']
        crud.fill_db(data)

        return {'message': f'Database filled successfully'}


@app.route('/boss/<int:number>', methods=['GET'])
def get_boss(number):
    data = crud.get_boss_data(number)
    return render_template("boss.html", employee=data['employee_info'], boss=data['boss'], subordinates=data['subordinates'])


@app.route('/get_data', methods=['GET'])
def get_data():
    all_employees = crud.get_employees()
    employee_list = []
    for row in all_employees:
        employee_dict = {
            'id': row.id,
            'surname': row.surname,
            'name': row.name,
            'patronymic': row.patronymic,
            'position': row.position,
            'start_work_date': row.start_work_date,
            'salary': row.salary,
            'boss_id': row.boss_id,
            'boss_surname': row.boss_surname,
            'boss_name': row.boss_name,
            'boss_patronymic': row.boss_patronymic
        }
        if employee_dict['boss_name'] is None:
            continue
        employee_list.append(employee_dict)

    # Print the results
    return render_template('employees.html', employees=employee_list)

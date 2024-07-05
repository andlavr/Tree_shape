from flask import request, redirect, render_template, url_for, jsonify

from app.app import app, db
from app.models import Employees
from crud.fake_data import surname, personal_name, patronymic, salary_, job

# @app.route('/')
# def main():
#     return {'Test':'test'}

@app.route('/', methods=['GET'])
def index():
    return {'message': 'Hello!'}

@app.route('/employees', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        print('Add new employee')
        data = request.get_json()
        new_employee = Employees(surname=data['surname'], name=data['name'], patronymic=data['patronymic'],
                                 salary=data['salary'], job=data['job'], start_work_date=data['start_work_date'])
        db.session.add(new_employee)
        db.session.commit()
        db.session.refresh(new_employee)
        return {'message': f'Employee {new_employee.id} was added to database'}
    else:
        return {'message': 'Payload is invalid'}






if __name__ == '__main__':
    app.run(debug=True)


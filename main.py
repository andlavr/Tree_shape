from flask import request, flash, redirect, render_template, url_for, jsonify

from app.app import app, db
from app.models import Employees
from crud.fake_data import surname, personal_name, patronymic, salary_, job

# @app.route('/')
# def main():
#     return {'Test':'test'}

@app.route('/', methods=['GET'])
def index():
    posts = Employees.query.all()
    return render_template("index.html", posts=posts)
@app.route('/posts', methods=['GET','POST'])
def add_to_db(surname, personal_name, patronymic, salary_, job):
    if request.method == 'POST':
        surname = surname['surname']
        name = personal_name['name']
        patronymic = patronymic['patronymic']
        salary = salary_['salary']
        job = job['job']
        new_data = Employees(surname=surname, name=personal_name, patronymic=patronymic,
                            salary=salary_, job=job)
        db.session.add(new_data)
        db.session.commit()
        flash('Added')
    return redirect(url_for('index'))





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


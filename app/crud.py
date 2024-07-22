import traceback

from sqlalchemy.orm import aliased

from app.app import db
from app.db_loader import Tree
from app.models import Employees, SubordinationLinks


def get_employees():
    boss = aliased(Employees)
    employee = aliased(Employees)

    # Perform the query
    results = db.session.query(
        employee.id,
        employee.surname,
        employee.name,
        employee.patronymic,
        employee.position,
        employee.start_work_date,
        employee.salary,
        boss.id.label('boss_id'),
        boss.surname.label('boss_surname'),
        boss.name.label('boss_name'),
        boss.patronymic.label('boss_patronymic')
    ).outerjoin(
        SubordinationLinks,
        SubordinationLinks.employer_id == employee.id
    ).outerjoin(
        boss,
        SubordinationLinks.boss_id == boss.id
    ).all()

    return results

def get_boss_data(employee_id):
    boss = aliased(Employees)
    employee = aliased(Employees)
    subordinate = aliased(Employees)

    # Query to get the boss of the employee
    boss_info = db.session.query(
        boss.id,
        boss.surname,
        boss.name,
        boss.patronymic,
        boss.position
    ).join(
        SubordinationLinks,
        SubordinationLinks.boss_id == boss.id
    ).filter(
        SubordinationLinks.employer_id == employee_id
    ).first()

    # Query to get the subordinates of the employee
    subordinates_info = db.session.query(
        subordinate.id,
        subordinate.surname,
        subordinate.name,
        subordinate.patronymic,
        subordinate.position
    ).join(
        SubordinationLinks,
        SubordinationLinks.employer_id == subordinate.id
    ).filter(
        SubordinationLinks.boss_id == employee_id
    ).all()

    # Query to get the employee details
    employee_info = db.session.query(
        employee.id,
        employee.surname,
        employee.name,
        employee.patronymic,
        employee.position,
        employee.start_work_date,
        employee.salary
    ).filter(
        employee.id == employee_id
    ).first()

    print(boss_info)

    return {"boss": boss_info, "subordinates": subordinates_info, "employee_info": employee_info}


def add_employer(data, commit=True):
    employer = Employees(
        surname=data['surname'],
        name=data['name'],
        patronymic=data['patronymic'],
        salary=data['salary'],
        position=data['position'],
        start_work_date=data['start_work_date']
    )
    db.session.add(employer)
    if commit: db.session.commit()

    return employer


def add_subordination_links(data, commit=True):
    links = SubordinationLinks(boss_id=data[0], employer_id=data[1])
    db.session.add(links)
    if commit: db.session.commit()

    return True


def fill_db(data):
    """

    :param data:
    :return:
    """

    tree = Tree.from_json(data)

    for i in range(5):
        nodes_at_depth = tree.get_nodes_at_depth(i)
        for parent in nodes_at_depth:
            parent_id = add_employer(parent.value, commit=True).id
            for child in parent.children:
                child_id = add_employer(child.value, commit=True).id
                print(parent_id, child_id)
                add_subordination_links([parent_id, child_id], commit=True)

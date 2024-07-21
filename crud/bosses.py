from app.app import app
from app.models import Employees, Bosses
from app.models import db
import random

with app.app_context() as context:
    ids = db.session.query(Employees.id).all()

    two_ids = random.choices(ids, k=2)
    print(two_ids)












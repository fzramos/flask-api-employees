from faker import Faker

def getProfile():
    fake = Faker()
    return fake.profile()

import os
from employee_api.models import Employee
from employee_api import db

def seedData():
    for seed_num in range(10):
        data = getProfile()
        employee = Employee(data['name'], data['mail'], data['ssn'], data['job'], data['sex'])
        db.session.add(employee)
        db.session.commit()
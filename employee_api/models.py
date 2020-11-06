from employee_api import app, db, ma, login_manager

from datetime import datetime

import uuid

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    ssn = db.Column(db.String, nullable = False)
    job = db.Column(db.String, nullable = False)
    sex = db.Column(db.String, nullable = False)

    def __init__(self, full_name, email, ssn, job, sex, id = id):
        self.full_name = full_name
        self.email = email
        self.ssn = ssn
        self.job = job
        self.sex = sex
        # self.id = id

    def __repr__(self):
        return f'Added new employee {self.full_name} with the email {self.email} added to the database.'

class EmployeeSchema(ma.Schema):
    class Meta:
        # create fields that will show after dat digested
        fields = ['id', 'full_name', 'job', 'sex', 'email', 'address', 'ssn']

employee_schema = EmployeeSchema()
# if you want 1 employee

employees_schema = EmployeeSchema(many = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(200), primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), nullable = False)
    hash = db.Column(db.String(256), nullable = False)
    token = db.Column(db.String(400))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token_refreshed = db.Column(db.Boolean, default = False)
    date_refreshed = db.Column(db.DateTime)

    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.hash = self.set_password(password)

    def set_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f'New user {self.name} created with the email is {self.email}.'
from employee_api import app, db, ma, login_manager

from datetime import datetime

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

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)


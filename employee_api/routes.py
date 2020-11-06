from employee_api import app, db
from employee_api.models import Employee, employee_schema, employees_schema, User, check_password_hash
from flask import jsonify, request, render_template, url_for, redirect
from employee_api.forms import UserForm, LoginForm

from flask_login import login_required, login_user, current_user, logout_user

import jwt

from datetime import datetime

from employee_api.forms import UserForm, LoginForm

from employee_api.token_verification import token_required

# Enpoint for CREATING an employee
@app.route('/employees/create', methods = ['POST'])
@token_required
def create_employee(current_user_token):
    name = request.json['full_name']
    email = request.json['email']
    ssn = request.json['ssn']
    job = request.json['job']
    sex = request.json['sex']
    address = request.json['address']

    emp = Employee(name, email, ssn, job, sex, address)
    db.session.add(emp)
    db.session.commit()

    results = employee_schema.dump(emp)
    return jsonify(results)

# Endpoint for RETREIVING all employee's info
@app.route('/employees', methods = ['GET'])
@token_required
def get_employees(current_user_token):
    employees = Employee.query.all()
    return jsonify(employees_schema.dump(employees))

# Endpoint for RETREIVING 1 specific employee's info
@app.route('/employees/<id>', methods = ['GET'])
@token_required
def get_employee(current_user_token, id):
    employee = Employee.query.get(id)
    return jsonify(employee_schema.dump(employee))

# Endpoint for UPDATING 1 specific employee's info
@app.route('/employees/update/<id>', methods = ['POST'])
@token_required
def update_employee(current_user_token, id):
    emp = Employee.query.get(id)

    # would like to only update employee properties that are included in posted json
    # but having trouble implementing it
    # for key, value in request.json.items():
    #     emp.key = value
    #     doesn't work since key is a string

    emp.full_name = request.json['full_name']
    emp.email = request.json['email']
    emp.ssn = request.json['ssn']
    emp.job = request.json['job']
    emp.sex = request.json['sex']
    emp.address = request.json['address']

    db.session.commit()

    return employee_schema.jsonify(emp)

# Endpoint for DELETING 1 specific employee's info
@app.route('/employees/delete/<id>', methods = ['DELETE'])
@token_required
def delete_employee(current_user_token, id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify(employee_schema.dump(emp))

@app.route('/users/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect('/users/login')

    return render_template('register.html', form = form)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        print(0)
        # user = User(name, email, password)
        user = User.query.filter(User.email == email).first()
        # print(user)
        # print(check_password_hash(password, user.hash))
        if user and check_password_hash(user.hash, password):
            print('1')
            login_user(user)
            return redirect('/users/token')
            # return redirect('/token')

    return render_template('login.html', form = form)

@app.route('/users/token')
@login_required
def get_token():
    token = jwt.encode({
        'public_id': current_user.id,
        'email': current_user.email,
    }, app.config['SECRET_KEY'])
    user = User.query.get(current_user.id)
    user.token = token
    user.date_created = datetime.utcnow()
    
    db.session.commit()

    results = token.decode('utf-8')
    return render_template('token.html', token = token)

@app.route('/users/tokenupdate')
@login_required
def refresh_token():
    refresh_key = {'refreshToken': jwt.encode({
        'public_id': current_user.id,
        'email': current_user.email,
    }, app.config['SECRET_KEY'])}
    # token = jwt.encode({
    #     'public_id': current_user.id,
    #     'email': current_user.email,
    # }, app.config['SECRET_KEY'])
    temp = refresh_key.get('refreshToken')
    new_token = temp.decode('utf-8')

    user = User.query.get(current_user.id)
    user.token = new_token
    user.token_refreshed = True
    user.date_refreshed = datetime.utcnow()

    db.session.commit()

    return render_template('token.html', token = new_token)

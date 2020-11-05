from employee_api import app, db
from employee_api.models import Employee, employee_schema, employees_schema
from flask import jsonify, request

# Enpoint for CREATING an employee
@app.route('/employees/create', methods = ['POST'])
def create_employee():
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
def get_employees():
    employees = Employee.query.all()
    return jsonify(employees_schema.dump(employees))

# Endpoint for RETREIVING 1 specific employee's info
@app.route('/employees/<id>', methods = ['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return jsonify(employee_schema.dump(employee))

# Endpoint for UPDATING 1 specific employee's info
@app.route('/employees/update/<id>', methods = ['POST'])
def update_employee(id):
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
def delete_employee(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify(employee_schema.dump(emp))

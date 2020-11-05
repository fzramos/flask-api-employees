from employee_api import app
from faker_seed_db import seedData

if __name__ == '__main__':
    app.run(debug = True)
    # seedData()
    # run this function to get 10 new employees in Employee db
    # comment out if you don't want to add more
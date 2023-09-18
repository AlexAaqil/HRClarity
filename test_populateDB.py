from hrms import create_app, db
from hrms.models import Employee, Leave, Department, Occupation
from datetime import datetime

app = create_app()

# Test data for departments
department1 = Department(name='Computer')
department2 = Department(name='Accounts')
department3 = Department(name='Management')

# Test data for occupations
occupation1 = Occupation(name='Web Developer', department_id=1)
occupation2 = Occupation(name='UI/UX Developer', department_id=1)
occupation3 = Occupation(name='Accountant', department_id=2)

# Create test data for employees
employee1 = Employee(first_name='John', last_name='Doe', gender='Male', dob=datetime(1990, 1, 15), email_address='johndoe@gmail.com', phone_number='+254 746 055 498', national_id=11111111, occupation_id=1)
employee2 = Employee(first_name='Jane', last_name='Smith', dob=datetime(1985, 5, 20), gender='Female', email_address='jane@example.com', phone_number='9876543210', national_id=22222222, occupation_id=2)
employee3 = Employee(first_name='Diane', last_name='Johnson', dob=datetime(1995, 4, 24), gender='Female', email_address='diane@gmail.com', phone_number='9876543210', national_id=33333333, occupation_id=3)

# test data for leaves
leave1 = Leave(leave_type='Study', from_date=datetime(2023, 7, 1), to_date=datetime(2023, 7, 10), employee_id=1)
leave2 = Leave(leave_type='Sick', from_date=datetime(2023, 9, 22), to_date=datetime(2023, 9, 25), employee_id=2)

# Add data to the database
with app.app_context():
    db.session.add(department1)
    db.session.add(department2)
    db.session.add(department3)
    db.session.add(occupation1)
    db.session.add(occupation2)
    db.session.add(occupation3)
    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)
    db.session.add(leave1)
    db.session.add(leave2)
    db.session.commit()

print('Test data added to the database.')

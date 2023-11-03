from hrms import create_app, db, bcrypt
from hrms.models import User, Leave, Department, Occupation, Announcement
from datetime import datetime

app = create_app()

# Test data for departments
department1 = Department(name='Computer')
department2 = Department(name='Accounts')
department3 = Department(name='Management')
department4 = Department(name='Human Resource')
department5 = Department(name='Social Work')

# Test data for occupations
occupation1 = Occupation(name='Web Developer', department_id=1)
occupation2 = Occupation(name='UI/UX Developer', department_id=1)
occupation3 = Occupation(name='Accountant', department_id=2)
occupation4 = Occupation(name='HR Manager', department_id=4)
occupation5 = Occupation(name='Counsellor', department_id=5)

# Create test data for employees
temporary_password = "employee"
hashed_password = bcrypt.generate_password_hash(temporary_password).decode('utf-8')
employee1 = User(first_name='John', last_name='Doe', gender='Male', dob=datetime(1990, 1, 15), email_address='johndoe@gmail.com', phone_number='+254 746 055 498', national_id=11111111, occupation_id=1, password=hashed_password, image_file="default.jpg")
employee2 = User(first_name='Jane', last_name='Smith', dob=datetime(1985, 5, 20), gender='Female', email_address='jane@example.com', phone_number='0798 765 431', national_id=22222222, occupation_id=2, password=hashed_password, image_file="default.jpg")
employee3 = User(first_name='Diane', last_name='Johnson', dob=datetime(1995, 4, 24), gender='Female', email_address='diane@gmail.com', phone_number='+256 871 540 210', national_id=33333333, occupation_id=3, password=hashed_password, image_file="default.jpg")
employee4 = User(first_name='Zoey', last_name='Johnson', dob=datetime(1993, 7, 11), gender='Female', email_address='zoey@gmail.com', phone_number='+254 987 654 321', national_id=44444444, occupation_id=1, password=hashed_password, image_file="default.jpg")
employee5 = User(first_name='Evans', last_name='Prestine', dob=datetime(1993, 9, 13), gender='Male', email_address='evans@gmail.com', phone_number='+254 987 654 321', national_id=55555555, occupation_id=3, password=hashed_password, image_file="default.jpg")
employee6 = User(first_name='Elizabeth', last_name='Keen', dob=datetime(1985, 5, 23), gender='Female', email_address='elizabeth@gmail.com', phone_number='+254 984 614 301', national_id=66666666, occupation_id=5, password=hashed_password, image_file="default.jpg")
employee7 = User(first_name='HR', last_name='Manager', dob=datetime(1985, 5, 20), gender='Female', email_address='hrm@gmail.com', phone_number='+254 925 612 101', national_id=77777777, occupation_id=4, user_level = 2, user_type='hrm', password=hashed_password, image_file="default.jpg")

# test data for leaves
leave1 = Leave(leave_type='Study', from_date=datetime(2023, 7, 1), to_date=datetime(2023, 7, 10), employee_id=1)
leave2 = Leave(leave_type='Sick', from_date=datetime(2023, 9, 22), to_date=datetime(2023, 9, 25), employee_id=5)
leave3 = Leave(leave_type='Sabbatical', from_date=datetime(2023, 9, 24), to_date=datetime(2023, 11, 11), employee_id=4)
leave4 = Leave(leave_type='Study', from_date=datetime(2023, 9, 22), to_date=datetime(2023, 10, 10), employee_id=5)

# test data for announcements
announcement1 = Announcement(title='General Meeting', content='All employees to meet at the Union Hall tomorrow at 10:00 A.M', ends_at=datetime(2023, 9, 25))
announcement2 = Announcement(title='Recruitments', content='Recruitments for promotions to be held at the Union Hall today from 08:00 A.M to 16:00 P.M', ends_at=datetime(2023, 9, 26))

# Add data to the database
with app.app_context():
    db.session.add(department1)
    db.session.add(department2)
    db.session.add(department3)
    db.session.add(department4)
    db.session.add(department5)
    db.session.add(occupation1)
    db.session.add(occupation2)
    db.session.add(occupation3)
    db.session.add(occupation4)
    db.session.add(occupation5)
    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)
    db.session.add(employee4)
    db.session.add(employee5)
    db.session.add(employee6)
    db.session.add(employee7)
    db.session.add(leave1)
    db.session.add(leave2)
    db.session.add(leave3)
    db.session.add(leave4)
    db.session.add(announcement1)
    db.session.add(announcement2)
    db.session.commit()

print('Test data added to the database.')

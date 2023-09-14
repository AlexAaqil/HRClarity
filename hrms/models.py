from datetime import datetime
from flask_login import UserMixin
from hrms import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin

    employee = Employee.query.get(int(user_id))
    if employee:
        return employee

    return None


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship
    occupations = db.relationship('Occupation', backref='department', lazy=True)

    def __repr__(self):
        return f"Department('{self.name}')"


class Occupation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Relationship
    employees = db.relationship('Employee', backref='occupation', lazy=True)

    def __repr__(self):
        return f"Occupation('{self.name}')"


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.first_name}', '{self.last_name}', '{self.email_address}')"


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(7), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    national_id = db.Column(db.Integer, nullable=False)
    occupation_id = db.Column(db.Integer, db.ForeignKey('occupation.id'), nullable=False)
    user_level = db.Column(db.Integer, nullable=False, default=1)
    leaves = db.relationship('Leave')

    # Relationships
    employee_occupation = db.relationship('Occupation', backref='employees_occupation', overlaps="employees,occupation", foreign_keys=[occupation_id])

    def __repr__(self):
        return f"Employee('{self.first_name}', '{self.last_name}', '{self.email_address}')"


class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_type = db.Column(db.String(40), nullable=False)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    status = db.Column(db.String(12), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Leave('{self.leave_type}', '{self.created_at}')"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.created_at}')"

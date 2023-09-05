from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from hrms import db, bcrypt
from hrms.admin.forms import AdminLoginForm, AdminSignupForm, AddEmployeeForm
from hrms.models import Admin, Employee


admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email_address=form.email_address.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Oops! Check your credentials!', 'danger')
    return render_template('login.html', page_title='Admin Login', form=form)


@admin.route('/admin/signup', methods=['GET', 'POST'])
def signup():
    form = AdminSignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(first_name=form.first_name.data, last_name=form.last_name.data, email_address=form.email_address.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash('Your account has been created! You can now login', 'success')
        return redirect(url_for('admin.login'))
    return render_template('admin/signup.html', page_title='Admin Signup', form=form)


@admin.route('/admin/dashboard')
def admin_dashboard():
    employee_count = Employee.query.count()
    return render_template('admin/dashboard.html', page_title='Admin Dashboard', employee_count=employee_count, user=current_user)


@admin.route('/admin/add_employee')
def add_employee():
    form = AddEmployeeForm()
    return render_template('add_employee.html', page_title='Add Employee', form=form, user=current_user)


@admin.route('/admin/employees')
def employees():
    employees = [
        {
            "first_name":"Alex",
            "last_name":"Wambui",
            "department":"computer",
            "occupation":"Web Developer"
        },
        {
            "first_name":"Flo",
            "last_name":"Muhoho",
            "department":"computer",
            "occupation":"Web Developer"
        },
        {
            "first_name":"Evans",
            "last_name":"Waweru",
            "department":"computer",
            "occupation":"Web Developer"
        },
        {
            "first_name":"Joyce",
            "last_name":"Nyambura",
            "department":"computer",
            "occupation":"Web Developer"
        },
        {
            "first_name":"Erick",
            "last_name":"Muli",
            "department":"computer",
            "occupation":"Web Developer"
        },
    ]
    return render_template('employees.html', page_title='Employees', employees=employees, user=current_user)
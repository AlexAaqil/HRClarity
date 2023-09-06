from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from hrms import bcrypt
from hrms.employee.forms import LoginForm
from hrms.models import Employee, Announcement


employee = Blueprint('employee', __name__)
employee_login_manager = LoginManager()

@employee_login_manager.user_loader
def load_employee_user(user_id):
    return Employee.query.get(int(user_id))


@employee.route('/employee/login', methods=['GET', 'POST'])
def employee_login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email_address=form.email_address.data).first()
        if employee and form.password.data == str(employee.national_id):
            login_user(employee)
            return redirect(url_for('employee.employee_dashboard'))
        else:
            flash('Oops! Check your credentials!', 'danger')

    return render_template('employee/login.html', page_title='Employee Login', form=form)


@employee.route('/employee/logout')
def logout():
    logout_user()
    return redirect(url_for('employee.employee_login'))


@employee.route('/employee/dashboard')
def employee_dashboard():
    announcements_count = Announcement.query.count()
    return render_template('employee/dashboard.html', page_title='Employee Dashboard', announcements_count=announcements_count, user=current_user)
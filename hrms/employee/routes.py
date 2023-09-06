from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user
from hrms import bcrypt
from hrms.employee.forms import Login
from hrms.models import Employee


employee = Blueprint('employee', __name__)


@employee.route('/employee/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email_address=form.email_address.data).first()
        if employee and form.password.data == str(employee.national_id):
            login_user(employee)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Oops! Check your credentials!', 'danger')
    return render_template('login.html', page_title='Employee Login', form=form)
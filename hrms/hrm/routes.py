from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hrms import db, bcrypt
from hrms.hrm.forms import CreateUserForm, UpdateEmployeeForm
from hrms.models import User, Department, Occupation, Announcement, Leave


admin = Blueprint('admin', __name__)


@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    employees_count = User.query.filter(User.user_level == 1).count()
    departments_count = Department.query.count()
    occupations_count = Occupation.query.count()

    today = datetime.now().date()
    announcements = Announcement.query.filter(Announcement.ends_at >= today).order_by(Announcement.ends_at.asc()).all()
    announcements_count = Announcement.query.count()

    latest_pending_leaves = db.session.query(Leave, User).join(User).filter(Leave.status == 'pending').order_by(Leave.created_at.desc()).limit(4).all()
    leaves_count = Leave.query.count()
    return render_template('admin/dashboard.html', page_title='Admin Dashboard', employees_count=employees_count, departments_count=departments_count, occupations_count=occupations_count, announcements=announcements, announcements_count=announcements_count,latest_pending_leaves=latest_pending_leaves, leaves_count=leaves_count, user=current_user)


@admin.route('/admin/employees')
@login_required
def employees():
    employees = db.session.query(User, Occupation).join(Occupation).filter(User.user_level == 1).order_by(User.first_name.asc()).all()
    employees_count = len(employees)
    return render_template('admin/employees.html', page_title='Employees', employees=employees, employees_count=employees_count, user=current_user)


@admin.route('/admin/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = CreateUserForm()
    if form.validate_on_submit():
        temporary_password = "employee"
        hashed_password = bcrypt.generate_password_hash(
            temporary_password).decode('utf-8')
        employee = User(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, dob=form.dob.data, email_address=form.email_address.data,
                        phone_number=form.phone_number.data, national_id=form.national_id.data, occupation_id=form.occupation.data, password=hashed_password)
        db.session.add(employee)
        db.session.commit()
        flash('Employee has been added!', 'success')
        return redirect(url_for('admin.employees'))

    return render_template('admin/add_employee.html', page_title='Add Employee', form=form, user=current_user)


@admin.route('/admin/employees/<int:employee_id>/update', methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = User.query.get_or_404(employee_id)
    form = UpdateEmployeeForm()
    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.gender = form.gender.data
        employee.dob = form.dob.data
        employee.email_address = form.email_address.data
        employee.phone_number = form.phone_number.data
        employee.national_id = form.national_id.data
        employee.occupation_id = form.occupation.data
        employee.user_level = form.user_level.data
        db.session.commit()
        flash('Employee has been updated!', 'success')
        return redirect(url_for('admin.employees', employee_id=employee.id))
    elif request.method == 'GET':
        form.first_name.data = employee.first_name
        form.last_name.data = employee.last_name
        form.gender.data = employee.gender
        form.dob.data = employee.dob
        form.email_address.data = employee.email_address
        form.phone_number.data = employee.phone_number
        form.national_id.data = employee.national_id
        form.occupation.data = str(employee.occupation_id)  # Convert to str for SelectField
        form.user_level.data = str(employee.user_level)  # Convert to str for SelectField

    return render_template('admin/add_employee.html', page_title='Update Employee', form=form, user=current_user)


@admin.route('/admin/employees/<int:employee_id>/delete', methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = User.query.get_or_404(employee_id)

    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Employee has been deleted!', 'success')
        return redirect(url_for('admin.employees'))

    return render_template('admin/employees.html', page_title='Employees')

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hrms import db, bcrypt
from hrms.hrm.forms import LoginForm, SignupForm, EmployeeForm, UpdateEmployeeForm
from hrms.models import Admin, Employee, Department, Occupation, Announcement, Leave


admin = Blueprint('admin', __name__)
hrm_login_manager = LoginManager()

@hrm_login_manager.user_loader
def load_hrm_user(user_id):
    return Admin.query.get(int(user_id))


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email_address=form.email_address.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Oops! Check your credentials!', 'danger')

    return render_template('admin/login.html', page_title='Admin Login', form=form)


@admin.route('/admin/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(first_name=form.first_name.data, last_name=form.last_name.data, email_address=form.email_address.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash('Your account has been created! You can now login', 'success')
        return redirect(url_for('admin.admin_login'))
    return render_template('admin/signup.html', page_title='Admin Signup', form=form)


@admin.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    employees_count = Employee.query.count()
    departments_count = Department.query.count()
    occupations_count = Occupation.query.count()

    today = datetime.now().date()
    announcements = Announcement.query.filter(Announcement.ends_at >= today).order_by(Announcement.ends_at.asc()).all()
    announcements_count = Announcement.query.count()

    latest_pending_leaves = db.session.query(Leave, Employee).join(Employee).filter(Leave.status == 'pending').order_by(Leave.created_at.desc()).limit(4).all()
    leaves_count = Leave.query.filter_by(status = 'pending').count()
    return render_template('admin/dashboard.html', page_title='Admin Dashboard', employees_count=employees_count, departments_count=departments_count, occupations_count=occupations_count, announcements=announcements, announcements_count=announcements_count,latest_pending_leaves=latest_pending_leaves, leaves_count=leaves_count, user=current_user)


@admin.route('/admin/employees')
@login_required
def employees():
    employees = db.session.query(Employee, Occupation).join(Occupation).order_by(Employee.first_name.asc()).all()
    employees_count = len(employees)
    return render_template('admin/employees.html', page_title='Employees', employees=employees, employees_count=employees_count, user=current_user)


@admin.route('/admin/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, dob=form.dob.data, email_address=form.email_address.data, phone_number=form.phone_number.data, national_id=form.national_id.data, occupation_id=form.occupation.data, user_level=form.user_level.data)
        db.session.add(employee)
        db.session.commit()
        flash('Employee has been added!', 'success')
        return redirect(url_for('admin.employees'))

    return render_template('admin/add_employee.html', page_title='Add Employee', form=form, user=current_user)


@admin.route('/admin/employees/<int:employee_id>/update', methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
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
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Employee has been deleted!', 'success')
        return redirect(url_for('admin.employees'))

    return render_template('admin/employees.html', page_title='Employees')

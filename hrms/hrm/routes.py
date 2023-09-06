from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hrms import db, bcrypt
from hrms.hrm.forms import LoginForm, SignupForm, EmployeeForm, DepartmentForm, OccupationForm, AnnouncementForm
from hrms.models import Admin, Employee, Department, Occupation, Announcement


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
        return redirect(url_for('admin.login'))
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
    announcements_count = Announcement.query.count()
    return render_template('admin/dashboard.html', page_title='Admin Dashboard', employees_count=employees_count, departments_count=departments_count, occupations_count=occupations_count, announcements_count=announcements_count, user=current_user)


@admin.route('/admin/employees')
@login_required
def employees():
    employees = Employee.query.all()
    employees_count = Employee.query.count()
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
    form = EmployeeForm()
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


@admin.route('/admin/departments')
@login_required
def departments():
    departments = Department.query.order_by(Department.name).all()
    departments_count = Department.query.count()
    return render_template('admin/departments.html', page_title='Departments', departments=departments, departments_count=departments_count, user=current_user)


@admin.route('/admin/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Department was added successfully!', 'success')
        return redirect(url_for('admin.departments'))

    return render_template('admin/add_department.html', page_title='Add Department', form=form, user=current_user)


@admin.route('/admin/departments/<int:department_id>/update', methods=['GET', 'POST'])
@login_required
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm()
    if form.validate_on_submit():
        department.name = form.name.data
        db.session.commit()
        flash('Department has been updated!', 'success')
        return redirect(url_for('admin.departments', department_id=department.id))
    elif request.method == 'GET':
        form.name.data = department.name

    return render_template('admin/add_department.html', page_title='Update Department', form=form, user=current_user)


@admin.route('/admin/departments/<int:department_id>/delete', methods=['POST'])
@login_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)

    if request.method == 'POST':
        db.session.delete(department)
        db.session.commit()
        flash('Department has been deleted!', 'success')
        return redirect(url_for('admin.departments'))

    return render_template('admin/departments.html', page_title='Departments')


@admin.route('/admin/occupations')
@login_required
def occupations():
    occupations = Occupation.query.order_by(Occupation.name).all()
    occupations_count = Occupation.query.count()
    return render_template('admin/occupations.html', page_title='Occupations', occupations=occupations, occupations_count=occupations_count, user=current_user)


@admin.route('/admin/occupations/add', methods=['GET', 'POST'])
@login_required
def add_occupation():
    form = OccupationForm()
    if form.validate_on_submit():
        occupation = Occupation(name=form.name.data, department_id = form.department_id.data)
        db.session.add(occupation)
        db.session.commit()
        flash('Occupation was added successfully!', 'success')
        return redirect(url_for('admin.occupations'))

    return render_template('admin/add_occupation.html', page_title='Add Occupation', form=form, user=current_user)


@admin.route('/admin/occupations/<int:occupation_id>/update', methods=['GET', 'POST'])
@login_required
def update_occupation(occupation_id):
    occupation = Occupation.query.get_or_404(occupation_id)
    form = OccupationForm()
    if form.validate_on_submit():
        occupation.name = form.name.data
        occupation.department_id = form.department_id.data
        db.session.commit()
        flash('Occupation has been updated!', 'success')
        return redirect(url_for('admin.occupations', occupation_id=occupation.id))
    elif request.method == 'GET':
        form.name.data = occupation.name
        form.department_id.data = str(occupation.department_id)

    return render_template('admin/add_occupation.html', page_title='Update Occupation', form=form, user=current_user)


@admin.route('/admin/occupations/<int:occupation_id>/delete', methods=['POST'])
@login_required
def delete_occupation(occupation_id):
    occupation = Occupation.query.get_or_404(occupation_id)

    if request.method == 'POST':
        db.session.delete(occupation)
        db.session.commit()
        flash('Occupation has been deleted!', 'success')
        return redirect(url_for('admin.occupations'))

    return render_template('admin/occupations.html', page_title='Occupations')


@admin.route('/admin/announcements')
@login_required
def announcements():
    announcements = Announcement.query.order_by(Announcement.created_at).all()
    announcements_count = Announcement.query.count()
    return render_template('announcements.html', page_title='Announcements', announcements=announcements, announcements_count=announcements_count, user=current_user)


@admin.route('/admin/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content = form.content.data, ends_at=form.ends_at.data)
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement was added successfully!', 'success')
        return redirect(url_for('admin.announcements'))

    return render_template('admin/add_announcement.html', page_title='Add Announcement', form=form, user=current_user)


@admin.route('/admin/announcements/<int:announcement_id>/update', methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        announcement.ends_at = form.ends_at.data
        db.session.commit()
        flash('Announcement has been updated!', 'success')
        return redirect(url_for('admin.announcements', announcement_id=announcement.id))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
        form.ends_at.data = announcement.ends_at

    return render_template('admin/add_announcement.html', page_title='Update Announcement', form=form, user=current_user)


@admin.route('/admin/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)

    if request.method == 'POST':
        db.session.delete(announcement)
        db.session.commit()
        flash('Announcement has been deleted!', 'success')
        return redirect(url_for('admin.announcements'))

    return render_template('announcements.html', page_title='Announcements')
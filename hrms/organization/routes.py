from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from hrms import db
from hrms.models import Department, Occupation
from hrms.organization.forms import DepartmentForm, OccupationForm


organization = Blueprint('organization', __name__)


@organization.route('/admin/departments')
@login_required
def departments():
    departments = Department.query.order_by(Department.name).all()
    departments_count = Department.query.count()
    return render_template('admin/departments.html', page_title='Departments', departments=departments, departments_count=departments_count, user=current_user)


@organization.route('/admin/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Department was added successfully!', 'success')
        return redirect(url_for('organization.departments'))

    return render_template('admin/add_department.html', page_title='Add Department', form=form, user=current_user)


@organization.route('/admin/departments/<int:department_id>/update', methods=['GET', 'POST'])
@login_required
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm()
    if form.validate_on_submit():
        department.name = form.name.data
        db.session.commit()
        flash('Department has been updated!', 'success')
        return redirect(url_for('organization.departments', department_id=department.id))
    elif request.method == 'GET':
        form.name.data = department.name

    return render_template('admin/add_department.html', page_title='Update Department', form=form, user=current_user)


@organization.route('/admin/departments/<int:department_id>/delete', methods=['POST'])
@login_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)

    if request.method == 'POST':
        db.session.delete(department)
        db.session.commit()
        flash('Department has been deleted!', 'success')
        return redirect(url_for('organization.departments'))

    return render_template('admin/departments.html', page_title='Departments')


@organization.route('/admin/occupations')
@login_required
def occupations():
    occupations = Occupation.query.order_by(Occupation.name).all()
    occupations_count = Occupation.query.count()
    return render_template('admin/occupations.html', page_title='Occupations', occupations=occupations, occupations_count=occupations_count, user=current_user)


@organization.route('/admin/occupations/add', methods=['GET', 'POST'])
@login_required
def add_occupation():
    form = OccupationForm()
    if form.validate_on_submit():
        occupation = Occupation(name=form.name.data, department_id = form.department_id.data)
        db.session.add(occupation)
        db.session.commit()
        flash('Occupation was added successfully!', 'success')
        return redirect(url_for('organization.occupations'))

    return render_template('admin/add_occupation.html', page_title='Add Occupation', form=form, user=current_user)


@organization.route('/admin/occupations/<int:occupation_id>/update', methods=['GET', 'POST'])
@login_required
def update_occupation(occupation_id):
    occupation = Occupation.query.get_or_404(occupation_id)
    form = OccupationForm()
    if form.validate_on_submit():
        occupation.name = form.name.data
        occupation.department_id = form.department_id.data
        db.session.commit()
        flash('Occupation has been updated!', 'success')
        return redirect(url_for('organization.occupations', occupation_id=occupation.id))
    elif request.method == 'GET':
        form.name.data = occupation.name
        form.department_id.data = str(occupation.department_id)

    return render_template('admin/add_occupation.html', page_title='Update Occupation', form=form, user=current_user)


@organization.route('/admin/occupations/<int:occupation_id>/delete', methods=['POST'])
@login_required
def delete_occupation(occupation_id):
    occupation = Occupation.query.get_or_404(occupation_id)

    if request.method == 'POST':
        db.session.delete(occupation)
        db.session.commit()
        flash('Occupation has been deleted!', 'success')
        return redirect(url_for('organization.occupations'))

    return render_template('admin/occupations.html', page_title='Occupations')

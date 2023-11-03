from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user
from hrms import db, bcrypt
from .forms import LoginForm, UpdateProfilePictureForm, UpdatePasswordForm
from .utils import save_picture
from hrms.models import User


user = Blueprint('user', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user.route('/login', methods=['GET', 'POST'])
@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email_address=form.email_address.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # check if the user is an admin
            if user.user_level == 2:
                login_user(user)
                return redirect(url_for('admin.admin_dashboard'))
            else:
                login_user(user)
                return redirect(url_for('employee.employee_dashboard'))
        else:
            flash('Oops! Check your credentials!', 'danger')

    return render_template('login.html', page_title='Login', form=form)


@user.route('/user/update_password/<int:employee_id>', methods=['GET', 'POST'])
def update_password(employee_id):
    employee = User.query.get_or_404(employee_id)
    password_form = UpdatePasswordForm()
    if password_form.validate_on_submit():
        password = password_form.new_password.data
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        employee.password = hashed_password
        db.session.commit()
        flash('Password has been updated!', 'success')
        return redirect(url_for('user.login'))

    return render_template('update_password.html', page_title='Update Password', password_form=password_form, user=current_user)


@user.route('/user/update_profile/<int:employee_id>', methods=['GET', 'POST'])
def update_profile(employee_id):
    employee = User.query.get_or_404(employee_id)
    profile_picture = url_for('static', filename='images/profile_pictures/' + employee.image_file)
    form = UpdateProfilePictureForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            employee.image_file = picture_file
        db.session.commit()
        flash('Profile Image has been updated!', 'success')
        return redirect(url_for('user.update_profile', employee_id=employee_id))

    return render_template('update_profile.html', page_title='Update Profile', form=form, profile_picture=profile_picture, user=employee)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

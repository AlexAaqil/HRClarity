import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
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


def get_profile_picture(employee_id):
    user = User.query.get_or_404(employee_id)
    profile_picture = url_for('static', filename='images/profile_pictures/' + user.image_file)
    return profile_picture


@user.route('/user/profile_settings/<int:employee_id>')
def profile_settings(employee_id):
    profile_picture = get_profile_picture(employee_id=employee_id)
    return render_template('profile_settings.html', page_title='Profile Settings', profile_picture=profile_picture, user=current_user)


@user.route('/user/update_password/<int:employee_id>', methods=['GET', 'POST'])
def update_password(employee_id):
    employee = User.query.get_or_404(employee_id)
    profile_picture = get_profile_picture(employee_id=employee_id)
    password_form = UpdatePasswordForm()
    if password_form.validate_on_submit():
        password = password_form.new_password.data
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        employee.password = hashed_password
        db.session.commit()
        flash('Password has been updated!', 'success')
        return redirect(url_for('user.login'))

    return render_template('update_password.html', page_title='Update Password', profile_picture=profile_picture, password_form=password_form, user=current_user)


@user.route('/user/update_profile/<int:employee_id>', methods=['GET', 'POST'])
def update_profile(employee_id):
    employee = User.query.get_or_404(employee_id)
    profile_picture = get_profile_picture(employee_id=employee_id)
    form = UpdateProfilePictureForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            if employee.image_file and employee.image_file != 'default.jpg':
                try:
                    old_profile_picture = os.path.join(current_app.root_path, 'static/images/profile_pictures', employee.image_file)
                    os.remove(old_profile_picture)
                except Exception as e:
                    print(f"Error deleting the old image: {e}")

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

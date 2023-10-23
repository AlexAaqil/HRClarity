from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hrms import db, bcrypt
from .forms import LoginForm
from hrms.models import User, Department, Occupation, Announcement, Leave


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


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

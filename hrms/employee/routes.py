from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hrms import bcrypt
from hrms.models import User, Announcement, Leave


employee = Blueprint('employee', __name__)


@employee.route('/employee/dashboard')
@login_required
def employee_dashboard():
    announcements_count = Announcement.query.count()
    leaves_count = len(Leave.query.filter_by(employee_id=current_user.id).all())
    return render_template('employee/dashboard.html', page_title='User Dashboard', announcements_count=announcements_count, leaves_count=leaves_count, user=current_user)
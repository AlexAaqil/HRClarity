from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from hrms import db
from hrms.leaves.forms import MakeLeaveRequest
from hrms.models import Leave, Employee


leaves = Blueprint('leaves', __name__)


@leaves.route('/employee/leaves')
@login_required
def employee_view_leaves():
    if current_user.is_authenticated:
        user = current_user.id
        leaves = Leave.query.filter_by(employee_id=user).order_by(Leave.created_at.desc()).all()
        leaves_count = len(leaves)
        return render_template('employee/leaves.html', page_title='Employee Leaves', leaves=leaves, leaves_count=leaves_count)


@leaves.route('/admin/leaves')
@login_required
def admin_view_leaves():
    leaves = db.session.query(Leave, Employee).join(Employee).all()
    leaves_count = len(leaves)
    pending_leaves = len([leave for leave, _ in leaves if leave.status == 'pending'])
    return render_template('admin/leaves.html', page_title='Leave Requests', leaves=leaves, leaves_count=leaves_count, pending_leaves=pending_leaves, user=current_user)


@leaves.route('/employee/leaves/request', methods=['GET', 'POST'])
@login_required
def make_leave_request():
    form = MakeLeaveRequest()
    if form.validate_on_submit():
        leave_request = Leave(leave_type=form.leave_type.data, from_date = form.from_date.data, to_date=form.to_date.data, employee_id=current_user.id)
        db.session.add(leave_request)
        db.session.commit()
        flash('Leave Request has been sent!', 'success')
        return redirect(url_for('leaves.employee_view_leaves', user_id=current_user.id))
    return render_template('employee/make_leave_request.html', page_title='Apply for Leave', form=form, user=current_user)


@leaves.route('/admin/leaves/approval/<int:leave_id>/<string:status>', methods=['POST'])
@login_required
def request_approval(leave_id, status):
    leave_request = Leave.query.get_or_404(leave_id)
    leave_request.status = status
    db.session.commit()
    flash(f'Leave request has been {status}!', 'success')
    return redirect(url_for('leaves.admin_view_leaves'))

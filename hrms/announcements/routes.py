from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from hrms import db
from hrms.announcements.forms import AnnouncementForm
from hrms.models import Announcement


announcements = Blueprint('announcements', __name__)


@announcements.route('/admin/announcements')
@login_required
def announcements():
    announcements = Announcement.query.order_by(Announcement.created_at).all()
    announcements_count = Announcement.query.count()
    return render_template('announcements.html', page_title='Announcements', announcements=announcements, announcements_count=announcements_count, user=current_user)


@announcements.route('/admin/announcements/add', methods=['GET', 'POST'])
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


@announcements.route('/admin/announcements/<int:announcement_id>/update', methods=['GET', 'POST'])
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


@announcements.route('/admin/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)

    if request.method == 'POST':
        db.session.delete(announcement)
        db.session.commit()
        flash('Announcement has been deleted!', 'success')
        return redirect(url_for('admin.announcements'))

    return render_template('announcements.html', page_title='Announcements')
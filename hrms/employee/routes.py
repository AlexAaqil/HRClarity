from flask import Blueprint, render_template
from hrms.employee.forms import Login


employee = Blueprint('employee', __name__)


@employee.route('/employee/login', methods=['GET', 'POST'])
def login():
    form = Login()
    return render_template('login.html', page_title='Employee Login', form=form)
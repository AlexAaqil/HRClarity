from flask import Blueprint, render_template
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('main/index.html')


@main.route('/about')
def about():
    return render_template('main/about.html')

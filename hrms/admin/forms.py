from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hrms.models import Admin

class AdminSignup(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder":"First Name", "class":"form-control"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder":"Last Name", "class":"form-control"})
    email_address = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder":"Email Address", "class":"form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password", "class":"form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder":"Confirm Password", "class":"form-control"})
    submit = SubmitField('Signup', render_kw={"class":"btn btn-primary btn-block"})

    def validate_email_address(self, email_address):
        user = Admin.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError('An account with that email already exists!')


class AdminLogin(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder":"Email Address", "class":"form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password", "class":"form-control"})
    submit = SubmitField('Login', render_kw={"class":"btn btn-primary btn-block"})
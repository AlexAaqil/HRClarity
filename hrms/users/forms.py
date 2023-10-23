from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email(
    )], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             "placeholder": "Password", "class": "form-control"})
    submit = SubmitField('Login', render_kw={
                         "class": "btn btn-primary btn-block"})

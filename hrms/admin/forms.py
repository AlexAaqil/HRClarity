from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hrms.models import Admin, Department, Occupation

class AdminSignupForm(FlaskForm):
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


class AdminLoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder":"Email Address", "class":"form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password", "class":"form-control"})
    submit = SubmitField('Login', render_kw={"class":"btn btn-primary btn-block"})


class AddEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%d-%m-%Y', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Ohter', 'Other')], validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    national_id = IntegerField('National ID', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    occupation = SelectField('Occupation', validators=[DataRequired()])
    user_level = SelectField('User Level', choices=[(1, 'Employee'), (2, 'HR Manager'), (3, 'Admin')], validators=[DataRequired()])

    def __init__(self):
        super(AddEmployeeForm, self).__init__()

        # Fetch departments and occupations from the database
        departments = Department.query.all()
        occupations = Occupation.query.all()

        # Create choices for the SelectFields
        self.department.choices = [(dept.id, dept.name) for dept in departments]
        self.occupation.choices = [(occ.id, occ.name) for occ in occupations]
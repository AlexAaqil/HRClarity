from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hrms.models import Admin, Department, Occupation, Employee

class SignupForm(FlaskForm):
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


class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder":"Email Address", "class":"form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password", "class":"form-control"})
    submit = SubmitField('Login', render_kw={"class":"btn btn-primary btn-block"})


class EmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"class":"form-control"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"class":"form-control"})
    dob = DateField('Date of Birth', validators=[DataRequired()], render_kw={"class":"form-control"})
    gender = SelectField('Gender', choices=[('none_selected', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()], render_kw={"class":"form-control"})
    email_address = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"class":"form-control"})
    phone_number = StringField('Phone Number', validators=[DataRequired()], render_kw={"class":"form-control"})
    national_id = IntegerField('National ID', validators=[DataRequired()], render_kw={"class":"form-control"})
    occupation = SelectField('Occupation', validators=[DataRequired()], render_kw={"class":"form-control"})
    user_level = SelectField('User Level', choices=[('none_selected', 'Select User Level'), (1, 'Employee'), (2, 'Admin')], validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Save Changes', render_kw={"class":"btn btn-primary btn-block"})

    def __init__(self):
        super(EmployeeForm, self).__init__()

        # Fetch occupations from the database
        occupations = Occupation.query.all()

        # Create choices for the SelectFields
        self.occupation.choices = [('none_selected', 'Select Occupation')] + [(str(occ.id), occ.name) for occ in occupations]

    def validate_email_address(self, email_address):
        employee = Employee.query.filter_by(email_address=email_address.data).first()
        if employee:
            raise ValidationError('An account with that email already exists!')

    def validate_dob(form, field):
        today = date.today()
        age_limit_date = today.replace(year=today.year - 18)

        if field.data > age_limit_date:
            raise ValidationError('Must be at least 18 years old.')


class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Save Changes', render_kw={"class":"btn btn-primary btn-block"})


class OccupationForm(FlaskForm):
    name = StringField('Occupation Name', validators=[DataRequired()], render_kw={"class":"form-control"})
    department_id = SelectField('Department', validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Save Changes', render_kw={"class":"btn btn-primary btn-block"})

    def __init__(self):
        super(OccupationForm, self).__init__()

        # Fetch departments from the database
        departments = Department.query.all()

        # Create choices for the Department SelectField
        self.department_id.choices = [('none_selected', 'Select Department')] + [(str(dept.id), dept.name) for dept in departments]

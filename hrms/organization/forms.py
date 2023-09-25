from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from hrms.models import Department


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
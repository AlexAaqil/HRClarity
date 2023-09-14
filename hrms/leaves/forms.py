from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class MakeLeaveRequest(FlaskForm):
    leave_type = SelectField('Leave Type', choices=[('Leave of absence', 'Leave of absence'), ('Sick', 'Sick'), ('Maternal', 'Maternal'), ('Study', 'Study'), ('Sabbatical', 'Sabbatical')], validators=[DataRequired()], render_kw={"class":"form-control"})
    from_date = DateField('From Date', validators=[DataRequired()], render_kw={"class":"form-control"})
    to_date = DateField('To Date', validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Save Changes', render_kw={"class":"btn btn-primary btn-block"})
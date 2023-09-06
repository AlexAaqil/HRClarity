from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)], render_kw={"class":"form-control"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"class":"form-control", "rows":5})
    ends_at = DateField('End Date', validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField('Save Changes', render_kw={"class":"btn btn-primary btn-block"})
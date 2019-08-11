from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HistoryForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Go')

from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm

# NoneOf(values, message=None, values_formatter=None)

class AdminConfigForm(FlaskForm):
    # updated_at = StringField('Updated_at', [validators.Length(min=4, max=100)])
    # comment = StringField('Comment', [validators.Length(min=4, max=100)])
    temp_chaudiere_failure = IntegerField('Temp Chaudiere Failure', [validators.NumberRange(min=4, max=100, message="min/max constraint exceed")])
    # temp_chaudiere_failure = StringField('Temp Chaudiere Failure', validators=[validators.required()])
    submit = SubmitField('Update')

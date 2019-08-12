from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm

# NoneOf(values, message=None, values_formatter=None)

class AdminConfigForm(FlaskForm):
    comment = StringField('Comment', [validators.Length(min=0, max=300)])
    temp_chaudiere_failure = IntegerField(
                                'Temp Chaudiere Failure',
                                [validators.NumberRange(min=60, max=80, message="min=60, max=80")])
    temp_chaudiere_failure_success = HiddenField('Temp Chaudiere Failure Succes')
    
    chaudiere_db_rotate_days= IntegerField(
                                'Rotate Chaudiere db every (days)',
                                [validators.NumberRange(min=1, max=10, message="min=1, max=10")])
    
    chaudiere_minute_db_rotate_days = IntegerField(
                                'Rotate ChaudiereMinute db every (days)', 
                                [validators.NumberRange(min=3, max=60, message="min=3, max=60")])
    
    # temp_chaudiere_failure = StringField('Temp Chaudiere Failure', validators=[validators.required()])
    submit = SubmitField('Update')

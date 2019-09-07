from wtforms import TextAreaField, BooleanField, StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm

# NoneOf(values, message=None, values_formatter=None)

class AdminConfigForm(FlaskForm):
    temp_chaudiere_failure = IntegerField(
                                'Temp Chaudiere Failure',
                                [validators.NumberRange(min=55, max=75, message="min=55, max=75")])
    
    chaudiere_db_rotate_hours= IntegerField(
                                'Rotate Chaudiere db every (hours)',
                                [validators.NumberRange(min=1, max=96, message="min=1, max=96")])
    
    chaudiere_minute_db_rotate_days = IntegerField(
                                'Rotate ChaudiereMinute db every (days)', 
                                [validators.NumberRange(min=1, max=60, message="min=1, max=60")])

    alerts_enable = BooleanField('Enable alerts (SMS / Email)')

    comment = TextAreaField('Comment', [validators.Length(min=0, max=300)])
    
    # submit = SubmitField('Update')

'''
Forms for the calendar
'''

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, TimeField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, InputRequired
from website.models import EVENT_TYPE_CHOICES


# Form - Add Event
class AddEventForm(FlaskForm):
    ''' Add Event Form '''

    # Form Fields
    event_type = SelectField(
        label='Event Type *', choices=EVENT_TYPE_CHOICES)
    person = SelectField(label='Person', coerce=int,
                         validators=[InputRequired()])
    date = DateField(label='Date *', format='%Y-%m-%d',
                     validators=[DataRequired()])
    time = TimeField(label='Time *', format='%H:%M',
                     validators=[DataRequired()])
    note = TextAreaField(label='Note')
    submit = SubmitField(label='Create New Event')

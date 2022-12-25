'''
Forms for the calendar
'''

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, TimeField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, InputRequired
from website.models import EVENT_TYPE_CHOICES
from website.calendar.query import possible_people


# Form - Add Event
class AddEventForm(FlaskForm):
    ''' Add Event Form '''

    # Form Fields
    event_type = SelectField(
        label='Event Type *', choices=EVENT_TYPE_CHOICES)
    person = SelectField(label='Person', choices=[('', '')]+[(k, v) for k, v in possible_people.items()],
                         validators=[InputRequired()])
    # person = IntegerField(label='Person ID')
    date = DateField(label='Date *', format='%Y-%m-%d',
                     validators=[DataRequired()])
    time = TimeField(label='Time *', format='%H:%M',
                     validators=[DataRequired()])
    note = TextAreaField(label='Note')
    submit = SubmitField(label='Create New Event')

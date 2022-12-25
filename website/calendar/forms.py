'''
Forms for the calendar
'''

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, TimeField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, InputRequired


# Form - Add Event
class AddEventForm(FlaskForm):
    ''' Add Event Form '''

    # Form Fields
    event_type = SelectField(label='Event Type *', coerce=int,
                             validators=[InputRequired()])
    person = SelectField(label='Person', coerce=int,
                         validators=[InputRequired()])
    start_date = DateField(label='Start Date *', format='%Y-%m-%d',
                           validators=[DataRequired()])
    start_time = TimeField(label='Start Time *', format='%H:%M',
                           validators=[DataRequired()])
    end_date = DateField(label='End Date *', format='%Y-%m-%d',
                         validators=[DataRequired()])
    end_time = TimeField(label='End Time *', format='%H:%M',
                         validators=[DataRequired()])
    note = TextAreaField(label='Note')
    submit = SubmitField(label='Create New Event')

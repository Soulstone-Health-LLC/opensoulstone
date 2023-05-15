"""
Calendar > Forms - This file contains the forms for the Calendar Blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, TimeField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, InputRequired


# Form - Add Event
class EventForm(FlaskForm):
    """Event Form"""

    # Form Fields
    event_type_id = SelectField(
        label="Event Type *",
        coerce=int,
        validators=[InputRequired()],
        render_kw={
            "class": "form-control select2 form-select",
            "placeholder": "Select Event Type",
        },
    )
    person = SelectField(
        label="Person",
        coerce=int,
        validators=[InputRequired()],
        render_kw={
            "class": "form-control select2 form-select",
            "placeholder": "Select Person",
        },
    )
    practitioner_id = SelectField(
        label="Practitioner",
        coerce=int,
        render_kw={
            "class": "form-control select2 form-select",
            "placeholder": "Select Practitioner",
        },
    )
    date = DateField(
        label="Start Date *", format="%Y-%m-%d", validators=[DataRequired()]
    )
    start_time = TimeField(
        label="Start Time *", format="%H:%M", validators=[DataRequired()]
    )
    note = TextAreaField(
        label="Note",
        render_kw={"placeholder": "Add any notes about the event here..."}
    )
    submit = SubmitField(label="Save Event")

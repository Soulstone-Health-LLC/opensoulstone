"""
Calendar > Forms - This file contains the forms for the Calendar Blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField, SelectField, DateField, TimeField,
    IntegerField
)
from wtforms import TextAreaField
from wtforms.validators import DataRequired


# Form - Add Event
class EventForm(FlaskForm):
    """Event Form"""

    # Form Fields
    event_type_id = SelectField(
        label="Event Type *",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"class": "form-control select2 form-select"},
    )
    person = SelectField(
        label="Person *",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"class": "form-control select2 form-select",
                   }
    )
    practitioner_id = SelectField(
        label="Practitioner *",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"class": "form-control select2 form-select",
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


# Form - Add Blocked Off Time
class BlockedOffTimeForm(FlaskForm):
    """Blocked Off Time Form"""

    # Form Fields
    practitioner_id = SelectField(
        label="Practitioner",
        coerce=int,
        render_kw={"class": "form-control select2 form-select",
                   },
    )
    date = DateField(
        label="Start Date *", format="%Y-%m-%d", validators=[DataRequired()]
    )
    start_time = TimeField(
        label="Start Time *", format="%H:%M", validators=[DataRequired()]
    )
    duration = IntegerField(
        label="Duration (minutes) *", validators=[DataRequired()], default=30
    )
    note = TextAreaField(
        label="Note",
        render_kw={"placeholder": "Add any notes about the event here..."}
    )
    submit = SubmitField(label="Save Blocked Off Time")

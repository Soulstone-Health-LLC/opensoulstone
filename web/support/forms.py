"""Support > Forms - Forms for the support views."""
# Imports
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, SelectField, EmailField, DateField,
    TextAreaField)
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import TextArea
from dictionary.general import (
    STATE_CHOICES, ROLE_CHOICES, PHONE_TYPE_CHOICES, USER_TYPE_CHOICES)


# Form - Support - Add New Practice
class AddPracticeForm(FlaskForm):
    """Add New Practice Form"""

    name = StringField(
        label="Practice Name *", validators=[DataRequired(), Length(min=2)]
    )
    biography = StringField(label="Practice Biography", widget=TextArea())
    address_1 = StringField(label="Address Line 1 *",
                            validators=[DataRequired()])
    address_2 = StringField(label="Address Line 2")
    city = StringField(label="City *", validators=[DataRequired()])
    state = SelectField(
        label="State *", choices=STATE_CHOICES, validators=[DataRequired()]
    )
    zipcode = StringField(label="Zipcode *", validators=[DataRequired()])
    phone_number = TelField(label="Practice Phone Number *",
                            validators=[DataRequired()])
    phone_type = SelectField(label="Phone Type *", choices=PHONE_TYPE_CHOICES)
    email = EmailField(label="Practice Email *",
                       validators=[Email(), DataRequired()])
    website = StringField(label="Practice Website")
    submit = SubmitField(label="Add New Practice")


# Form - Add Practice User
class PracticeUserForm(FlaskForm):
    """Add or Edit the User to the Practice Form"""

    role = SelectField(
        label="User Role *", choices=ROLE_CHOICES, validators=[DataRequired()]
    )
    user_type = SelectField(label="User Type *", choices=USER_TYPE_CHOICES)
    first_name = StringField(
        label="First Name *", validators=[DataRequired(),
                                          Length(min=2, max=150)]
    )
    middle_name = StringField(label="Middle Name")
    last_name = StringField(
        label="Last Name *", validators=[DataRequired(),
                                         Length(min=2, max=150)]
    )
    suffix_name = StringField(label="Suffix")
    email = EmailField(
        label="Email *", validators=[DataRequired(), Email(),
                                     Length(min=3, max=150)]
    )
    phone_number = TelField(label="Phone Number *",
                            validators=[DataRequired()])
    phone_type = SelectField(label="Phone Type *", choices=PHONE_TYPE_CHOICES)
    submit = SubmitField(label="Register Account")


# Form - Release Notes
class ReleaseNotesForm(FlaskForm):
    """Add or edit release notes form"""

    release_note_date = DateField(label="Release Note Date *",
                                  default=datetime.now(tz=timezone.utc).date(),
                                  validators=[DataRequired()])
    release_note_content = TextAreaField(label="Release Note *",
                                         validators=[DataRequired()],
                                         widget=TextArea(),
                                         render_kw={"rows": 10})
    submit = SubmitField(label="Save")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

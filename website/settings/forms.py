# soulstone/website/settings/forms.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, Email, InputRequired
from wtforms.widgets import TextArea
from website.models import STATE_CHOICES, PHONE_TYPE_CHOICES
from website.models import STATUS_CHOICES, ROLE_CHOICES


# ------------------------------------------------------------------------------
# Form -Edit Practice
# ------------------------------------------------------------------------------
class EditPracticeForm(FlaskForm):
    ''' Edit Practice Information Form '''
    name = StringField(label='Practice Name *',
                             validators=[DataRequired(),
                                         Length(min=2)])
    biography = StringField(label='Practice Biography',
                            widget=TextArea())
    address_1 = StringField(label='Address Line 1 *',
                            validators=[DataRequired()])
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City *',
                       validators=[DataRequired()])
    state = SelectField(label='State *',
                        choices=STATE_CHOICES,
                        validators=[DataRequired()])
    zipcode = StringField(label='Zipcode *',
                          validators=[DataRequired()])
    email = EmailField(label='Practice Email *',
                       validators=[Email()])
    website = StringField(label='Practice Website')
    phone = TelField(label='Practice Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=PHONE_TYPE_CHOICES)
    submit = SubmitField(label='Save Practice Information')


# ------------------------------------------------------------------------------
# Form - Practice User
# ------------------------------------------------------------------------------
class PracticeUserForm(FlaskForm):
    ''' Add or Edit a User to the Practice Form '''
    role = SelectField(label='User Role *',
                       choices=ROLE_CHOICES,
                       validators=[InputRequired()])
    first_name = StringField(label='First Name *',
                             validators=[DataRequired(),
                                         Length(min=2, max=150)])
    middle_name = StringField(label='Middle Name')
    last_name = StringField(label='Last Name *',
                            validators=[DataRequired(),
                                        Length(min=2, max=150)])
    suffix_name = StringField(label='Suffix')
    address_1 = StringField(label='Address Line 1')
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City')
    state = SelectField(label='State',
                        choices=STATE_CHOICES)
    zipcode = StringField(label='Zipcode')
    email = EmailField(label='Email *',
                       validators=[DataRequired(),
                                   Email(),
                                   Length(min=3, max=150)])
    phone_number = TelField(label='Phone Number *',
                            validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=PHONE_TYPE_CHOICES,
                             validators=[InputRequired()])
    status = SelectField(label='Status *',
                         choices=STATUS_CHOICES,
                         validators=[InputRequired()])
    submit = SubmitField(label='Save Account')


# ------------------------------------------------------------------------------
# Form - Add Charge
# ------------------------------------------------------------------------------
class AddChargeForm(FlaskForm):
    ''' Add Billable Charge to the Practice '''
    code = StringField(label='Code *',
                       validators=[DataRequired(),
                                   Length(min=2)])
    name = StringField(label='Charge Name *',
                       validators=[DataRequired(),
                                   Length(min=2)])
    description = StringField(label='Charge Description *',
                              widget=TextArea(),
                              validators=[DataRequired()])
    status = SelectField(label='Status *',
                         choices=STATUS_CHOICES)
    submit = SubmitField(label='Add New Charge')


# ------------------------------------------------------------------------------
# Form - Edit Charge
# ------------------------------------------------------------------------------
class EditChargeForm(FlaskForm):
    ''' Edit existing Charge to the Practice '''
    code = StringField(label='Code *',
                       validators=[DataRequired(),
                                   Length(min=2)])
    name = StringField(label='Charge Name *',
                       validators=[DataRequired(),
                                   Length(min=2)])
    description = StringField(label='Charge Description *',
                              widget=TextArea(),
                              validators=[DataRequired()])
    status = SelectField(label='Status *',
                         choices=STATUS_CHOICES)
    submit = SubmitField(label='Save Charge')


# Form - Add Event Type
class EventTypeForm(FlaskForm):
    ''' Add New Event Type to the Practice '''
    event_name = StringField(label='Event Type Name *',
                             validators=[DataRequired(),
                                         Length(min=2)])
    event_description = StringField(label='Event Type Description *',
                                    widget=TextArea(),
                                    validators=[DataRequired()])
    event_status = SelectField(label='Status *',
                               choices=STATUS_CHOICES)
    submit = SubmitField(label='Save Event Type')

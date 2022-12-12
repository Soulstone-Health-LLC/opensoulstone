# soulstone/website/support/forms.py


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import TextArea
from website.models import STATE_CHOICES, ROLE_CHOICES
from website.models import PHONE_TYPE_CHOICES


# ------------------------------------------------------------------------------
# Form - Support - Add New Practice
# ------------------------------------------------------------------------------
class AddPracticeForm(FlaskForm):
    ''' Add New Practice Form '''
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
    submit = SubmitField(label='Add New Practice')


# ------------------------------------------------------------------------------
# Form - Add Practice User
# ------------------------------------------------------------------------------
class AddPracticeUserForm(FlaskForm):
    ''' Add User to the Practice Form '''
    role = SelectField(label='User Role *',
                       choices=ROLE_CHOICES,
                       validators=[DataRequired()])
    first_name = StringField(label='First Name *',
                             validators=[DataRequired(),
                                         Length(min=2, max=150)])
    middle_name = StringField(label='Middle Name')
    last_name = StringField(label='Last Name *',
                            validators=[DataRequired(),
                                        Length(min=2, max=150)])
    suffix_name = StringField(label='Suffix')
    email = EmailField(label='Email *',
                       validators=[DataRequired(),
                                   Email(),
                                   Length(min=3, max=150)])
    phone = TelField(label='Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=PHONE_TYPE_CHOICES)
    submit = SubmitField(label='Register Account')

'''
Forms for the persons blueprint
'''


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import EmailField, DateField, SearchField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length
from website.models import GENDER_PRONOUN_CHOICES, STATE_CHOICES
from website.models import PHONE_TYPE_CHOICES, STATUS_CHOICES


# ------------------------------------------------------------------------------
# Form - Add New Person
# ------------------------------------------------------------------------------
class AddPersonForm(FlaskForm):
    ''' Add User to the Practice Form '''
    first_name = StringField(label='First Name *',
                             validators=[DataRequired(),
                                         Length(min=2, max=150)])
    middle_name = StringField(label='Middle Name')
    last_name = StringField(label='Last Name *',
                            validators=[DataRequired(),
                                        Length(min=2, max=150)])
    suffix_name = StringField(label='Suffix')
    date_of_birth = DateField(label='Date of Birth *',
                              validators=[DataRequired()])
    gender_identity = SelectField(label='Gender Identity',
                                  choices=GENDER_PRONOUN_CHOICES)
    address_1 = StringField(label='Address Line 1')
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City')
    state = SelectField(label='State',
                        choices=STATE_CHOICES)
    zipcode = StringField(label='Zipcode')
    email = EmailField(label='Email')
    phone = TelField(label='Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=PHONE_TYPE_CHOICES)
    submit = SubmitField(label='Create New Person')


# ------------------------------------------------------------------------------
# Form - Edit Person
# ------------------------------------------------------------------------------
class EditPersonForm(FlaskForm):
    ''' Add User to the Practice Form '''
    first_name = StringField(label='First Name *',
                             validators=[DataRequired(),
                                         Length(min=2, max=150)])
    middle_name = StringField(label='Middle Name')
    last_name = StringField(label='Last Name *',
                            validators=[DataRequired(),
                                        Length(min=2, max=150)])
    suffix_name = StringField(label='Suffix')
    date_of_birth = DateField(label='Date of Birth *',
                              validators=[DataRequired()])
    gender_identity = SelectField(label='Gender Identity',
                                  choices=GENDER_PRONOUN_CHOICES)
    address_1 = StringField(label='Address Line 1')
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City')
    state = SelectField(label='State',
                        choices=STATE_CHOICES)
    zipcode = StringField(label='Zipcode')
    email = EmailField(label='Email')
    phone = TelField(label='Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=PHONE_TYPE_CHOICES)
    status = SelectField(label='Status *',
                         choices=STATUS_CHOICES)
    submit = SubmitField(label='Edit Person')

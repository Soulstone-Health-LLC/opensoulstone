'''
    File name: forms.py
    Author: Rodney Gauna
    Date created: 2021-11-14
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from sqlalchemy.sql.expression import label
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import EmailField, DateField
from wtforms.fields.numeric import DecimalField, FloatField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from wtforms.widgets import TextArea
from .models import People


# ------------------------------------------------------------------------------
# Form Classes
# ------------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
    ''' Sign Up / Register User Form '''
    email = EmailField(label='Email *',
                       validators=[DataRequired(),
                                   Email(),
                                   Length(min=3, max=150)])
    first_name = StringField(label='First Name *',
                             validators=[DataRequired(),
                                         Length(min=2, max=150)])
    last_name = StringField(label='Last Name *',
                            validators=[DataRequired(),
                                        Length(min=2, max=150)])
    password = PasswordField(label='Password *',
                             validators=[DataRequired(),
                                         Length(min=6, max=50)])
    confirm_password = PasswordField(label='Confirm Password *',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Register Account')


class LoginForm(FlaskForm):
    ''' Login Form '''
    email = EmailField(label='Email *',
                       validators=[DataRequired(),
                                   Email()])
    password = PasswordField(label='Password *',
                             validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class ResetRequestForm(FlaskForm):
    ''' Request Reset Password Form '''
    email = StringField(label='Email *',
                        validators=[DataRequired()])
    submit = SubmitField(label='Request Password Reset')


class ResetPasswordForm(FlaskForm):
    ''' Reset Password Form'''
    password = PasswordField(label='Password *',
                             validators=[DataRequired(),
                                         Length(min=6, max=50)])
    confirm_password = PasswordField(label='Confirm Password *',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Reset Password')


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
                        choices=[('', ''),
                                 ("AL", "AL"),
                                 ("AK", "AK"),
                                 ("AZ", "AZ"),
                                 ("AR", "AR"),
                                 ("CA", "CA"),
                                 ("CO", "CO"),
                                 ("CT", "CT"),
                                 ("DC", "DC"),
                                 ("DE", "DE"),
                                 ("FL", "FL"),
                                 ("GA", "GA"),
                                 ("HI", "HI"),
                                 ("ID", "ID"),
                                 ("IL", "IL"),
                                 ("IN", "IN"),
                                 ("IA", "IA"),
                                 ("KS", "KS"),
                                 ("KY", "KY"),
                                 ("LA", "LA"),
                                 ("ME", "ME"),
                                 ("MD", "MD"),
                                 ("MA", "MA"),
                                 ("MI", "MI"),
                                 ("MN", "MN"),
                                 ("MS", "MS"),
                                 ("MO", "MO"),
                                 ("MT", "MT"),
                                 ("NE", "NE"),
                                 ("NV", "NV"),
                                 ("NH", "NH"),
                                 ("NJ", "NJ"),
                                 ("NM", "NM"),
                                 ("NY", "NY"),
                                 ("NC", "NC"),
                                 ("ND", "ND"),
                                 ("OH", "OH"),
                                 ("OK", "OK"),
                                 ("OR", "OR"),
                                 ("PA", "PA"),
                                 ("RI", "RI"),
                                 ("SC", "SC"),
                                 ("SD", "SD"),
                                 ("TN", "TN"),
                                 ("TX", "TX"),
                                 ("UT", "UT"),
                                 ("VT", "VT"),
                                 ("VA", "VA"),
                                 ("WA", "WA"),
                                 ("WV", "WV"),
                                 ("WI", "WI"),
                                 ("WY", "WY")],
                        validators=[DataRequired()])
    zipcode = StringField(label='Zipcode *',
                          validators=[DataRequired()])
    email = EmailField(label='Practice Email *',
                       validators=[Email()])
    website = StringField(label='Practice Website')
    phone = TelField(label='Practice Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=[('Office', 'Office'),
                                      ('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Fax', 'Fax')])
    submit = SubmitField(label='Add New Practice')


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
                        choices=[('', ''),
                                 ("AL", "AL"),
                                 ("AK", "AK"),
                                 ("AZ", "AZ"),
                                 ("AR", "AR"),
                                 ("CA", "CA"),
                                 ("CO", "CO"),
                                 ("CT", "CT"),
                                 ("DC", "DC"),
                                 ("DE", "DE"),
                                 ("FL", "FL"),
                                 ("GA", "GA"),
                                 ("HI", "HI"),
                                 ("ID", "ID"),
                                 ("IL", "IL"),
                                 ("IN", "IN"),
                                 ("IA", "IA"),
                                 ("KS", "KS"),
                                 ("KY", "KY"),
                                 ("LA", "LA"),
                                 ("ME", "ME"),
                                 ("MD", "MD"),
                                 ("MA", "MA"),
                                 ("MI", "MI"),
                                 ("MN", "MN"),
                                 ("MS", "MS"),
                                 ("MO", "MO"),
                                 ("MT", "MT"),
                                 ("NE", "NE"),
                                 ("NV", "NV"),
                                 ("NH", "NH"),
                                 ("NJ", "NJ"),
                                 ("NM", "NM"),
                                 ("NY", "NY"),
                                 ("NC", "NC"),
                                 ("ND", "ND"),
                                 ("OH", "OH"),
                                 ("OK", "OK"),
                                 ("OR", "OR"),
                                 ("PA", "PA"),
                                 ("RI", "RI"),
                                 ("SC", "SC"),
                                 ("SD", "SD"),
                                 ("TN", "TN"),
                                 ("TX", "TX"),
                                 ("UT", "UT"),
                                 ("VT", "VT"),
                                 ("VA", "VA"),
                                 ("WA", "WA"),
                                 ("WV", "WV"),
                                 ("WI", "WI"),
                                 ("WY", "WY")],
                        validators=[DataRequired()])
    zipcode = StringField(label='Zipcode *',
                          validators=[DataRequired()])
    email = EmailField(label='Practice Email *',
                       validators=[Email()])
    website = StringField(label='Practice Website')
    phone = TelField(label='Practice Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=[('Office', 'Office'),
                                      ('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Fax', 'Fax')])
    submit = SubmitField(label='Save Practice Information')


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
                                  choices=[('', ''),
                                           ('Male', 'Male'),
                                           ('Female', 'Female'),
                                           ('Female-to-male transsexual', 'Female-to-male transsexual '),
                                           ('Male-to-female transsexual', 'Male-to-female transsexual'),
                                           ('Identifies as non-conforming', 'Identifies as non-conforming'),
                                           ('Other', 'Other')])
    address_1 = StringField(label='Address Line 1')
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City')
    state = SelectField(label='State',
                        choices=[('', ''),
                                 ("AL", "AL"),
                                 ("AK", "AK"),
                                 ("AZ", "AZ"),
                                 ("AR", "AR"),
                                 ("CA", "CA"),
                                 ("CO", "CO"),
                                 ("CT", "CT"),
                                 ("DC", "DC"),
                                 ("DE", "DE"),
                                 ("FL", "FL"),
                                 ("GA", "GA"),
                                 ("HI", "HI"),
                                 ("ID", "ID"),
                                 ("IL", "IL"),
                                 ("IN", "IN"),
                                 ("IA", "IA"),
                                 ("KS", "KS"),
                                 ("KY", "KY"),
                                 ("LA", "LA"),
                                 ("ME", "ME"),
                                 ("MD", "MD"),
                                 ("MA", "MA"),
                                 ("MI", "MI"),
                                 ("MN", "MN"),
                                 ("MS", "MS"),
                                 ("MO", "MO"),
                                 ("MT", "MT"),
                                 ("NE", "NE"),
                                 ("NV", "NV"),
                                 ("NH", "NH"),
                                 ("NJ", "NJ"),
                                 ("NM", "NM"),
                                 ("NY", "NY"),
                                 ("NC", "NC"),
                                 ("ND", "ND"),
                                 ("OH", "OH"),
                                 ("OK", "OK"),
                                 ("OR", "OR"),
                                 ("PA", "PA"),
                                 ("RI", "RI"),
                                 ("SC", "SC"),
                                 ("SD", "SD"),
                                 ("TN", "TN"),
                                 ("TX", "TX"),
                                 ("UT", "UT"),
                                 ("VT", "VT"),
                                 ("VA", "VA"),
                                 ("WA", "WA"),
                                 ("WV", "WV"),
                                 ("WI", "WI"),
                                 ("WY", "WY")])
    zipcode = StringField(label='Zipcode')
    email = EmailField(label='Email')
    phone = TelField(label='Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=[('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Office', 'Office'),
                                      ('Fax', 'Fax')])
    submit = SubmitField(label='Create New Person')


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
                                  choices=[('', ''),
                                           ('Male', 'Male'),
                                           ('Female', 'Female'),
                                           ('Female-to-male transsexual', 'Female-to-male transsexual '),
                                           ('Male-to-female transsexual', 'Male-to-female transsexual'),
                                           ('Identifies as non-conforming', 'Identifies as non-conforming'),
                                           ('Other', 'Other')])
    address_1 = StringField(label='Address Line 1')
    address_2 = StringField(label='Address Line 2')
    city = StringField(label='City')
    state = SelectField(label='State',
                        choices=[('', ''),
                                 ("AL", "AL"),
                                 ("AK", "AK"),
                                 ("AZ", "AZ"),
                                 ("AR", "AR"),
                                 ("CA", "CA"),
                                 ("CO", "CO"),
                                 ("CT", "CT"),
                                 ("DC", "DC"),
                                 ("DE", "DE"),
                                 ("FL", "FL"),
                                 ("GA", "GA"),
                                 ("HI", "HI"),
                                 ("ID", "ID"),
                                 ("IL", "IL"),
                                 ("IN", "IN"),
                                 ("IA", "IA"),
                                 ("KS", "KS"),
                                 ("KY", "KY"),
                                 ("LA", "LA"),
                                 ("ME", "ME"),
                                 ("MD", "MD"),
                                 ("MA", "MA"),
                                 ("MI", "MI"),
                                 ("MN", "MN"),
                                 ("MS", "MS"),
                                 ("MO", "MO"),
                                 ("MT", "MT"),
                                 ("NE", "NE"),
                                 ("NV", "NV"),
                                 ("NH", "NH"),
                                 ("NJ", "NJ"),
                                 ("NM", "NM"),
                                 ("NY", "NY"),
                                 ("NC", "NC"),
                                 ("ND", "ND"),
                                 ("OH", "OH"),
                                 ("OK", "OK"),
                                 ("OR", "OR"),
                                 ("PA", "PA"),
                                 ("RI", "RI"),
                                 ("SC", "SC"),
                                 ("SD", "SD"),
                                 ("TN", "TN"),
                                 ("TX", "TX"),
                                 ("UT", "UT"),
                                 ("VT", "VT"),
                                 ("VA", "VA"),
                                 ("WA", "WA"),
                                 ("WV", "WV"),
                                 ("WI", "WI"),
                                 ("WY", "WY")])
    zipcode = StringField(label='Zipcode')
    email = EmailField(label='Email')
    phone = TelField(label='Phone Number *',
                     validators=[DataRequired()])
    phone_type = SelectField(label='Phone Type *',
                             choices=[('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Office', 'Office'),
                                      ('Fax', 'Fax')])
    status = SelectField(label='Status *',
                         choices=[('Active', 'Active'),
                                  ('Inactive', 'Inactive')])
    submit = SubmitField(label='Edit Person')


class AddPracticeUserForm(FlaskForm):
    ''' Add User to the Practice Form '''
    role = SelectField(label='User Role *',
                       choices=[('Practitioner', 'Practitioner'),
                                ('Staff', 'Staff')],
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
                             choices=[('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Office', 'Office'),
                                      ('Fax', 'Fax')])
    submit = SubmitField(label='Register Account')


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
                         choices=[('Active', 'Active'),
                                  ('Inactive', 'Inactive')])
    submit = SubmitField(label='Add New Charge')


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
                         choices=[('Active', 'Active'),
                                  ('Inactive', 'Inactive')])
    submit = SubmitField(label='Save Charge')

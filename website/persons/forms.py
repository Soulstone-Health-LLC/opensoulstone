# soulstone/website/persons/forms.py


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import EmailField, DateField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length


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


# ------------------------------------------------------------------------------
# Form -Edit Person
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

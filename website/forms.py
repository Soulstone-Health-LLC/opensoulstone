'''
    File name: forms.py
    Author: Rodney Gauna
    Date created: 2021-11-14
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import EmailField, DateField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.widgets import TextArea


# ------------------------------------------------------------------------------
# Form - User Registration
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


# ------------------------------------------------------------------------------
# Form - Login
# ------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    ''' Login Form '''
    email = EmailField(label='Email *',
                       validators=[DataRequired(),
                                   Email()])
    password = PasswordField(label='Password *',
                             validators=[DataRequired()])
    submit = SubmitField(label='Log In')


# ------------------------------------------------------------------------------
# Form - Request Password Reset
# ------------------------------------------------------------------------------
class ResetRequestForm(FlaskForm):
    ''' Request Reset Password Form '''
    email = StringField(label='Email *',
                        validators=[DataRequired()])
    submit = SubmitField(label='Request Password Reset')


# ------------------------------------------------------------------------------
# Form - Reset Password
# ------------------------------------------------------------------------------
class ResetPasswordForm(FlaskForm):
    ''' Reset Password Form'''
    password = PasswordField(label='Password *',
                             validators=[DataRequired(),
                                         Length(min=6, max=50)])
    confirm_password = PasswordField(label='Confirm Password *',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Reset Password')


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


# ------------------------------------------------------------------------------
# Form - Add Practice User
# ------------------------------------------------------------------------------
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
                         choices=[('Active', 'Active'),
                                  ('Inactive', 'Inactive')])
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
                         choices=[('Active', 'Active'),
                                  ('Inactive', 'Inactive')])
    submit = SubmitField(label='Save Charge')


# ------------------------------------------------------------------------------
# Form - Add Visit Note
# ------------------------------------------------------------------------------
class AddVisitNoteForm(FlaskForm):
    ''' Add new Visit Note '''
    date_of_service = DateField(label='Date of Service *',
                                validators=[DataRequired()])
    reason_for_visit = StringField(label='Reason for Visit')
    chakra_assessment_root_score = SelectField(label='Root Chakra Score',
                                               choices=[('', ''),
                                                        ('-5', -5),
                                                        ('-4', -4),
                                                        ('-3', -3),
                                                        ('-2', -2),
                                                        ('-1', -1),
                                                        ('0', 0),
                                                        ('1', 1),
                                                        ('2', 2),
                                                        ('3', 3),
                                                        ('4', 4),
                                                        ('5', 5)])
    chakra_assessment_root_description = StringField(label='Root Chakra Notes',
                                                     widget=TextArea())
    chakra_assessment_sacral_score = SelectField(label='Sacral Chakra Score',
                                                 choices=[('', ''),
                                                          ('-5', -5),
                                                          ('-4', -4),
                                                          ('-3', -3),
                                                          ('-2', -2),
                                                          ('-1', -1),
                                                          ('0', 0),
                                                          ('1', 1),
                                                          ('2', 2),
                                                          ('3', 3),
                                                          ('4', 4),
                                                          ('5', 5)])
    chakra_assessment_sacral_description = StringField(label='Sacral Chakra Notes',
                                                       widget=TextArea())
    chakra_assessment_solar_plexus_score = SelectField(label='Solar Plexus Chakra Score',
                                                       choices=[('', ''),
                                                                ('-5', -5),
                                                                ('-4', -4),
                                                                ('-3', -3),
                                                                ('-2', -2),
                                                                ('-1', -1),
                                                                ('0', 0),
                                                                ('1', 1),
                                                                ('2', 2),
                                                                ('3', 3),
                                                                ('4', 4),
                                                                ('5', 5)])
    chakra_assessment_solar_plexus_description = StringField(label='Solar Plexus Chakra Notes',
                                                             widget=TextArea())
    chakra_assessment_heart_score = SelectField(label='Heart Chakra Score',
                                                choices=[('', ''),
                                                        ('-5', -5),
                                                        ('-4', -4),
                                                        ('-3', -3),
                                                        ('-2', -2),
                                                        ('-1', -1),
                                                        ('0', 0),
                                                        ('1', 1),
                                                        ('2', 2),
                                                        ('3', 3),
                                                        ('4', 4),
                                                        ('5', 5)])
    chakra_assessment_heart_description = StringField(label='Heart Chakra Notes',
                                                     widget=TextArea())
    chakra_assessment_throat_score = SelectField(label='Throat Chakra Score',
                                                 choices=[('', ''),
                                                          ('-5', -5),
                                                          ('-4', -4),
                                                          ('-3', -3),
                                                          ('-2', -2),
                                                          ('-1', -1),
                                                          ('0', 0),
                                                          ('1', 1),
                                                          ('2', 2),
                                                          ('3', 3),
                                                          ('4', 4),
                                                          ('5', 5)])
    chakra_assessment_throat_description = StringField(label='Throat Chakra Notes',
                                                       widget=TextArea())
    chakra_assessment_third_eye_score = SelectField(label='Third-Eye Chakra Score',
                                                    choices=[('', ''),
                                                             ('-5', -5),
                                                             ('-4', -4),
                                                             ('-3', -3),
                                                             ('-2', -2),
                                                             ('-1', -1),
                                                             ('0', 0),
                                                             ('1', 1),
                                                             ('2', 2),
                                                             ('3', 3),
                                                             ('4', 4),
                                                             ('5', 5)])
    chakra_assessment_third_eye_description = StringField(label='Third-Eye Chakra Notes',
                                                          widget=TextArea())
    chakra_assessment_crown_score = SelectField(label='Chakra Score',
                                                choices=[('', ''),
                                                         ('-5', -5),
                                                         ('-4', -4),
                                                         ('-3', -3),
                                                         ('-2', -2),
                                                         ('-1', -1),
                                                         ('0', 0),
                                                         ('1', 1),
                                                         ('2', 2),
                                                         ('3', 3),
                                                         ('4', 4),
                                                         ('5', 5)])
    chakra_assessment_crown_description = StringField(label='Crown Chakra Notes',
                                                      widget=TextArea())
    visit_notes = StringField(label='Visit Note',
                              widget=TextArea())
    post_visit_recommendations = StringField(label='Post Visit Recommendations',
                                             widget=TextArea())
    submit = SubmitField(label='Create Visit Note')


class EditVisitNoteForm(FlaskForm):
    ''' Add new Visit Note '''
    date_of_service = DateField(label='Date of Service *',
                                validators=[DataRequired()])
    reason_for_visit = StringField(label='Reason for Visit',
                                   widget=TextArea())
    chakra_assessment_root_score = SelectField(label='Root Chakra Score',
                                               choices=[('', ''),
                                                        ('-5', -5),
                                                        ('-4', -4),
                                                        ('-3', -3),
                                                        ('-2', -2),
                                                        ('-1', -1),
                                                        ('0', 0),
                                                        ('1', 1),
                                                        ('2', 2),
                                                        ('3', 3),
                                                        ('4', 4),
                                                        ('5', 5)])
    chakra_assessment_root_description = StringField(label='Root Chakra Notes',
                                                     widget=TextArea())
    chakra_assessment_sacral_score = SelectField(label='Sacral Chakra Score',
                                                 choices=[('', ''),
                                                          ('-5', -5),
                                                          ('-4', -4),
                                                          ('-3', -3),
                                                          ('-2', -2),
                                                          ('-1', -1),
                                                          ('0', 0),
                                                          ('1', 1),
                                                          ('2', 2),
                                                          ('3', 3),
                                                          ('4', 4),
                                                          ('5', 5)])
    chakra_assessment_sacral_description = StringField(label='Sacral Chakra Notes',
                                                       widget=TextArea())
    chakra_assessment_solar_plexus_score = SelectField(label='Solar Plexus Chakra Score',
                                                       choices=[('', ''),
                                                                ('-5', -5),
                                                                ('-4', -4),
                                                                ('-3', -3),
                                                                ('-2', -2),
                                                                ('-1', -1),
                                                                ('0', 0),
                                                                ('1', 1),
                                                                ('2', 2),
                                                                ('3', 3),
                                                                ('4', 4),
                                                                ('5', 5)])
    chakra_assessment_solar_plexus_description = StringField(label='Solar Plexus Chakra Notes',
                                                             widget=TextArea())
    chakra_assessment_heart_score = SelectField(label='Heart Chakra Score',
                                                choices=[('', ''),
                                                        ('-5', -5),
                                                        ('-4', -4),
                                                        ('-3', -3),
                                                        ('-2', -2),
                                                        ('-1', -1),
                                                        ('0', 0),
                                                        ('1', 1),
                                                        ('2', 2),
                                                        ('3', 3),
                                                        ('4', 4),
                                                        ('5', 5)])
    chakra_assessment_heart_description = StringField(label='Heart Chakra Notes',
                                                     widget=TextArea())
    chakra_assessment_throat_score = SelectField(label='Throat Chakra Score',
                                                 choices=[('', ''),
                                                          ('-5', -5),
                                                          ('-4', -4),
                                                          ('-3', -3),
                                                          ('-2', -2),
                                                          ('-1', -1),
                                                          ('0', 0),
                                                          ('1', 1),
                                                          ('2', 2),
                                                          ('3', 3),
                                                          ('4', 4),
                                                          ('5', 5)])
    chakra_assessment_throat_description = StringField(label='Throat Chakra Notes',
                                                       widget=TextArea())
    chakra_assessment_third_eye_score = SelectField(label='Third-Eye Chakra Score',
                                                    choices=[('', ''),
                                                             ('-5', -5),
                                                             ('-4', -4),
                                                             ('-3', -3),
                                                             ('-2', -2),
                                                             ('-1', -1),
                                                             ('0', 0),
                                                             ('1', 1),
                                                             ('2', 2),
                                                             ('3', 3),
                                                             ('4', 4),
                                                             ('5', 5)])
    chakra_assessment_third_eye_description = StringField(label='Third-Eye Chakra Notes',
                                                          widget=TextArea())
    chakra_assessment_crown_score = SelectField(label='Chakra Score',
                                                choices=[('', ''),
                                                         ('-5', -5),
                                                         ('-4', -4),
                                                         ('-3', -3),
                                                         ('-2', -2),
                                                         ('-1', -1),
                                                         ('0', 0),
                                                         ('1', 1),
                                                         ('2', 2),
                                                         ('3', 3),
                                                         ('4', 4),
                                                         ('5', 5)])
    chakra_assessment_crown_description = StringField(label='Crown Chakra Notes',
                                                      widget=TextArea())
    visit_notes = StringField(label='Visit Note',
                              widget=TextArea())
    post_visit_recommendations = StringField(label='Post Visit Recommendations',
                                             widget=TextArea())
    submit = SubmitField(label='Save Visit Note')
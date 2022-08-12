# soulstone/website/support/forms.py


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import TextArea


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

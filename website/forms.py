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
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.widgets import TextArea


# ------------------------------------------------------------------------------
# Form Classes
# ------------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
    ''' Sign Up / Register User Form '''
    email = StringField(label='Email *',
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
    email = StringField(label='Email *',
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
    email = StringField(label='Practice Email *',
                        validators=[Email()])
    website = StringField(label='Practice Website')
    phone = StringField(label='Practice Phone Number *')
    phone_type = SelectField(label='Phone Type *',
                             choices=[('Mobile', 'Mobile'),
                                      ('Home', 'Home'),
                                      ('Office', 'Office'),
                                      ('Fax', 'Fax')])
    submit = SubmitField(label='Add New Practice')

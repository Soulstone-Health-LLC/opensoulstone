'''
    File name: forms.py
    Author: Rodney Gauna
    Date created: 2021-11-14
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


# ------------------------------------------------------------------------------
# Form Classes
# ------------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
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
    email = StringField(label='Email *',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField(label='Password *',
                             validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class ResetRequest(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField(label='Request Password Reset')


class ResetPassword(FlaskForm):
    password = PasswordField(label='Password *',
                             validators=[DataRequired(),
                                         Length(min=6, max=50)])
    confirm_password = PasswordField(label='Confirm Password *',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Reset Password')

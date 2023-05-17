"""
Terms of Service - User Agreement Forms
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField


# User Agreement Form
class UserAgreementForm(FlaskForm):
    """User Agreement Form"""
    submit = SubmitField("I Agree")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

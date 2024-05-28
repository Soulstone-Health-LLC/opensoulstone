"""
Terms of Service - User Agreement Forms
"""

# Imports
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, DateField
from wtforms.validators import DataRequired


# User Agreement Form
class UserAgreementForm(FlaskForm):
    """User Agreement Form"""
    submit = SubmitField("I Agree")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})


class TermsOfServiceForm(FlaskForm):
    """Terms of Service Form"""
    current_date = datetime.now()

    content = TextAreaField(
        "Content * (HTML)", render_kw={"rows": 10},
        validators=[DataRequired()])
    active_date = DateField(
        "Active Date *", format="%Y-%m-%d", validators=[DataRequired()])
    sunset_date = DateField("Sunset Date", format="%Y-%m-%d")
    version = StringField(
        "Version *", default=str(current_date), validators=[DataRequired()])
    submit = SubmitField("Save")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

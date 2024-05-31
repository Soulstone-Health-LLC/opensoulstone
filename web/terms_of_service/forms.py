"""Terms of Service - User Agreement Forms"""
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
    # Create a version number using the current date.
    version_number = datetime.now().strftime("%Y.%m.%d")

    content = TextAreaField(
        "Content * (HTML)", render_kw={"rows": 10},
        validators=[DataRequired()])
    active_date = DateField("Active Date *", validators=[DataRequired()])
    sunset_date = DateField("Sunset Date *", validators=[DataRequired()])
    version = StringField(
        "Version *", default=str(version_number), validators=[DataRequired()])
    submit = SubmitField("Save")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

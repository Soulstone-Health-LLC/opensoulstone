"""
Visit Notes > Forms - This file contains all of the forms for the Visit Notes
Blueprint.
"""

# Imports
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from src.dictionary.general import CHAKRA_SCORE_CHOICES


# Form - Add Visit Note
class AddVisitNoteForm(FlaskForm):
    """Add new Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()],
        default=datetime.today
    )
    reason_for_visit = StringField(label="Reason for Visit", widget=TextArea())
    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = StringField(
        label="Root Chakra Notes", widget=TextArea()
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = StringField(
        label="Sacral Chakra Notes", widget=TextArea()
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = StringField(
        label="Solar Plexus Chakra Notes", widget=TextArea()
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = StringField(
        label="Heart Chakra Notes", widget=TextArea()
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = StringField(
        label="Throat Chakra Notes", widget=TextArea()
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = StringField(
        label="Third-Eye Chakra Notes", widget=TextArea()
    )
    chakra_assessment_crown_score = SelectField(
        label="Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = StringField(
        label="Crown Chakra Notes", widget=TextArea()
    )
    visit_notes = StringField(label="Visit Note", widget=TextArea())
    post_visit_recommendations = StringField(
        label="Post Visit Recommendations", widget=TextArea()
    )
    submit = SubmitField(label="Create Visit Note")


# Form - Edit Visit Note
class EditVisitNoteForm(FlaskForm):
    """Edit Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()])
    reason_for_visit = StringField(label="Reason for Visit", widget=TextArea())
    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = StringField(
        label="Root Chakra Notes", widget=TextArea()
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = StringField(
        label="Sacral Chakra Notes", widget=TextArea()
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = StringField(
        label="Solar Plexus Chakra Notes", widget=TextArea()
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = StringField(
        label="Heart Chakra Notes", widget=TextArea()
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = StringField(
        label="Throat Chakra Notes", widget=TextArea()
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = StringField(
        label="Third-Eye Chakra Notes", widget=TextArea()
    )
    chakra_assessment_crown_score = SelectField(
        label="Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = StringField(
        label="Crown Chakra Notes", widget=TextArea()
    )
    visit_notes = StringField(label="Visit Note", widget=TextArea())
    post_visit_recommendations = StringField(
        label="Post Visit Recommendations", widget=TextArea()
    )
    submit = SubmitField(label="Save Visit Note")

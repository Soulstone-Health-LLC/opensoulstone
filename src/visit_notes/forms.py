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
from src.dictionary.general import (
    CHAKRA_SCORE_CHOICES, VISIT_NOTE_STATUS_CHOICES
)


# Form - Add Visit Note
class AddVisitNoteForm(FlaskForm):
    """Add new Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()],
        default=datetime.today
    )
    reason_for_visit = StringField(label="Reason for Visit", widget=TextArea(),
                                   render_kw={"rows": 5})
    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = StringField(
        label="Root Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = StringField(
        label="Sacral Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = StringField(
        label="Solar Plexus Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = StringField(
        label="Heart Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = StringField(
        label="Throat Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = StringField(
        label="Third-Eye Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_crown_score = SelectField(
        label="Crown Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = StringField(
        label="Crown Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    visit_notes = StringField(label="Visit Note", widget=TextArea(),
                              render_kw={"rows": 10})
    post_visit_recommendations = StringField(
        label="Post Visit Recommendations", widget=TextArea(),
        render_kw={"rows": 10}
    )
    submit = SubmitField(label="Create Visit Note")


# Form - Edit Visit Note
class EditVisitNoteForm(FlaskForm):
    """Edit Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()])
    reason_for_visit = StringField(label="Reason for Visit", widget=TextArea(),
                                   render_kw={"rows": 5})
    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = StringField(
        label="Root Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = StringField(
        label="Sacral Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = StringField(
        label="Solar Plexus Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = StringField(
        label="Heart Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = StringField(
        label="Throat Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = StringField(
        label="Third-Eye Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    chakra_assessment_crown_score = SelectField(
        label="Crown Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = StringField(
        label="Crown Chakra Notes", widget=TextArea(),
        render_kw={"rows": 5}
    )
    visit_notes = StringField(label="Visit Note", widget=TextArea(),
                              render_kw={"rows": 10})
    post_visit_recommendations = StringField(
        label="Post Visit Recommendations", widget=TextArea(),
        render_kw={"rows": 10}
    )
    submit = SubmitField(label="Save Visit Note")


# Form - Change Visit Note Status
class ChangeVisitNoteStatusForm(FlaskForm):
    """Change Visit Note Status"""

    status = SelectField(label="Status", choices=VISIT_NOTE_STATUS_CHOICES)
    submit = SubmitField(label="Change Status")


# Form - Delete Visit Note
class DeleteVisitNoteForm(FlaskForm):
    """Delete Visit Note"""

    submit = SubmitField(label="Delete Visit Note")

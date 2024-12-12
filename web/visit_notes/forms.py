"""
Visit Notes > Forms - This file contains all of the forms for the Visit Notes
Blueprint.
"""

# Imports
from datetime import datetime
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from dictionary.general import (
    CHAKRA_SCORE_CHOICES, VISIT_NOTE_STATUS_CHOICES
)


# Form - Add Visit Note
class AddVisitNoteForm(FlaskForm):
    """Add new Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()],
        default=datetime.today
    )
    reason_for_visit = CKEditorField(label="Reason for Visit",
                                     render_kw={"rows": 5})

    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = CKEditorField(
        label="Root Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = CKEditorField(
        label="Sacral Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = CKEditorField(
        label="Solar Plexus Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = CKEditorField(
        label="Heart Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = CKEditorField(
        label="Throat Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = CKEditorField(
        label="Third-Eye Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_crown_score = SelectField(
        label="Crown Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = CKEditorField(
        label="Crown Chakra Notes",
        render_kw={"rows": 5}
    )
    visit_notes = CKEditorField(label="Visit Note",
                                render_kw={"rows": 10})

    post_visit_recommendations = CKEditorField(
        label="Post Visit Recommendations",
        render_kw={"rows": 10}
    )

    submit = SubmitField(label="Create Visit Note")


# Form - Edit Visit Note
class EditVisitNoteForm(FlaskForm):
    """Edit Visit Note"""

    date_of_service = DateField(
        label="Date of Service *", validators=[DataRequired()],
        default=datetime.today
    )
    reason_for_visit = CKEditorField(label="Reason for Visit",
                                     render_kw={"rows": 5})

    chakra_assessment_root_score = SelectField(
        label="Root Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_root_description = CKEditorField(
        label="Root Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_sacral_score = SelectField(
        label="Sacral Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_sacral_description = CKEditorField(
        label="Sacral Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_solar_plexus_score = SelectField(
        label="Solar Plexus Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_solar_plexus_description = CKEditorField(
        label="Solar Plexus Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_heart_score = SelectField(
        label="Heart Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_heart_description = CKEditorField(
        label="Heart Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_throat_score = SelectField(
        label="Throat Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_throat_description = CKEditorField(
        label="Throat Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_third_eye_score = SelectField(
        label="Third-Eye Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_third_eye_description = CKEditorField(
        label="Third-Eye Chakra Notes",
        render_kw={"rows": 5}
    )
    chakra_assessment_crown_score = SelectField(
        label="Crown Chakra Score", choices=CHAKRA_SCORE_CHOICES
    )
    chakra_assessment_crown_description = CKEditorField(
        label="Crown Chakra Notes",
        render_kw={"rows": 5}
    )
    visit_notes = CKEditorField(label="Visit Note",
                                render_kw={"rows": 10})

    post_visit_recommendations = CKEditorField(
        label="Post Visit Recommendations",
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

"""Visit Notes models"""
# Import
from datetime import datetime, timezone
from app import db


class Notes(db.Model):
    """SQL Table: notes"""

    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    date_of_service = db.Column(db.DateTime, nullable=False)
    reason_for_visit = db.Column(db.Text)
    chakra_assessment_root_score = db.Column(db.Integer)
    chakra_assessment_root_description = db.Column(db.Text)
    chakra_assessment_sacral_score = db.Column(db.Integer)
    chakra_assessment_sacral_description = db.Column(db.Text)
    chakra_assessment_solar_plexus_score = db.Column(db.Integer)
    chakra_assessment_solar_plexus_description = db.Column(db.Text)
    chakra_assessment_heart_score = db.Column(db.Integer)
    chakra_assessment_heart_description = db.Column(db.Text)
    chakra_assessment_throat_score = db.Column(db.Integer)
    chakra_assessment_throat_description = db.Column(db.Text)
    chakra_assessment_third_eye_score = db.Column(db.Integer)
    chakra_assessment_third_eye_description = db.Column(db.Text)
    chakra_assessment_crown_score = db.Column(db.Integer)
    chakra_assessment_crown_description = db.Column(db.Text)
    visit_notes = db.Column(db.Text)
    post_visit_recommendations = db.Column(db.Text)
    # Signed Status
    status = db.Column(db.Text, nullable=False, default="Open")

"""Settings models"""
# Import
from datetime import datetime, timezone
from app import db


class TermsOfService(db.Model):
    """SQL Table: terms_of_service"""

    __tablename__ = "terms_of_services"
    id = db.Column(db.Integer, primary_key=True)
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Active/Sunset Dates
    active_date = db.Column(db.DateTime(timezone=True), nullable=False)
    sunset_date = db.Column(db.DateTime(timezone=True))
    # Data Points - Main
    version = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)


class UserAgreement(db.Model):
    """SQL Table: user_agreement"""

    __tablename__ = "user_agreements"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tos_id = db.Column(db.Integer, db.ForeignKey("terms_of_services.id"))
    agreed_date = db.Column(db.DateTime(timezone=True))

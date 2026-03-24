"""Settings models"""
# Import
from datetime import datetime, timezone
from app import db


class Practice(db.Model):
    """SQL Table: practice"""

    __tablename__ = "practices"
    id = db.Column(db.Integer, primary_key=True)
    # Data Points - Created/Updated
    created_date = db.Column(db.DateTime(timezone=True), nullable=False,
                             default=datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    name = db.Column(db.Text, nullable=False)
    biography = db.Column(db.Text)
    address_1 = db.Column(db.Text, nullable=False)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    phone_type = db.Column(db.String(20), nullable=False)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    status = db.Column(db.Text, nullable=False, default="Active")

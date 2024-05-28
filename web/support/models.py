"""Settings models"""
# Import
from datetime import datetime, timezone
from app import db


class ReleaseNotes(db.Model):
    """SQL Table: release_notes"""

    __tablename__ = "release_notes"

    id = db.Column(db.Integer, primary_key=True)
    release_note_date = db.Column(db.Date, nullable=False)
    release_note_content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime(timezone=True))

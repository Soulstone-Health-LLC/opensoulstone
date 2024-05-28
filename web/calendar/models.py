"""Calendar events models"""
# Import
from datetime import datetime, timedelta, timezone
from app import db


class Events(db.Model):
    """SQL Table: events"""

    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_type_id = db.Column(db.Integer, db.ForeignKey("event_types.id"))
    practitioner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    note = db.Column(db.Text)


class EventTypes(db.Model):
    """SQL Table: event_types"""

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_name = db.Column(db.Text, nullable=False)
    event_description = db.Column(db.Text)
    event_status = db.Column(db.Text, nullable=False, default="Active")
    event_duration = db.Column(
        db.Interval, nullable=False, default=timedelta(minutes=30)
    )

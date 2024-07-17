"""Billing models"""
# Import
from datetime import datetime, timezone
from app import db


class Charges(db.Model):
    """SQL Table: charges"""

    __tablename__ = "charges"

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(),
                           default=datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime())
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    code = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float)
    status = db.Column(db.Text, default="Active")


class LedgerCharges(db.Model):
    """SQL Table: ledger_charges"""

    __tablename__ = "ledger_charges"

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"))
    charge_id = db.Column(db.Integer, db.ForeignKey("charges.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(),
                           default=datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime())
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    units = db.Column(db.Integer, nullable=False, default=1)
    unit_amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=0.0)


class LedgerPayments(db.Model):
    """SQL Table: ledger_payments"""

    __tablename__ = "ledger_payments"

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(),
                           default=datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime())
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)
    check_number = db.Column(db.String(50))
    credit_card_last_four = db.Column(db.Integer)
    payment_note = db.Column(db.Text)

"""
Functions for the person header
"""


# Imports
from flask_login import current_user
from app import db
from persons.models import People
from visit_notes.models import Notes
from events.models import Events
from billing.models import LedgerCharges, LedgerPayments


# Base Person Header
def personHeader(person_id):
    """Base person header"""
    person_header = (
        db.session.query(
            People.id,
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            People.address_1,
            People.address_2,
            People.city,
            People.state,
            People.zipcode,
            People.phone_number,
            People.phone_type,
            People.email,
            People.status,
            People.date_of_birth,
            People.gender_identity,
            People.profile_image,
        )
        .filter_by(id=person_id)
        .first()
    )

    # Visit Notes
    notes_count = Notes.query.filter_by(person_id=person_id).count()

    # Events
    events_count = Events.query.filter_by(person_id=person_id).count()

    # Ledger Charges
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0

    balance = total_charges - total_payments

    return (
        person_header,
        notes_count,
        events_count,
        balance,
    )

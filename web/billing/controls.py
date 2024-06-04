"""Billing > Controls - Controls for the billing blueprint."""
# Imports
from sqlalchemy.sql import select, func
from persons.models import People
from app import db
from .models import Charges, LedgerCharges, LedgerPayments


# Control - Get People
def get_people(practice_id):
    """Get people for a practice."""
    return People.query.filter_by(practice_id=practice_id).all()


# Control - Get Ledger Charges
def get_ledger_charges(practice_id, start_date):
    """Get ledger charges for a practice since a start date."""
    return (
        db.session.query(
            LedgerCharges.id,
            LedgerCharges.created_at,
            LedgerCharges.units,
            LedgerCharges.unit_amount,
            LedgerCharges.tax_rate,
            LedgerCharges.practice_id,
            People.id.label("person_id"),
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            People.gender_identity,
            Charges.code,
            Charges.description,
        )
        .join(People, LedgerCharges.person_id == People.id)
        .join(Charges, LedgerCharges.charge_id == Charges.id)
        .filter(LedgerCharges.practice_id == practice_id,
                LedgerCharges.created_at >= start_date)
        .all()
    )


# Control - Get Total Charges
def get_total_charges(practice_id):
    """Get total charges for a practice."""
    return (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=practice_id)
        .scalar()
    )


# Control - Get Total Payments
def get_total_payments(practice_id):
    """Get total payments for a practice."""
    return (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=practice_id)
        .scalar()
    )


# Control - Get Outstanding Balances
def get_outstanding_balances(practice_id):
    """Get people with outstanding balances for a practice."""
    charges_subquery = db.session.query(
        LedgerCharges.person_id,
        LedgerCharges.practice_id,
        db.func.sum(
            LedgerCharges.units * LedgerCharges.unit_amount
            + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
        ).label('total_charges')
    ).group_by(LedgerCharges.person_id, LedgerCharges.practice_id).subquery()

    payments_subquery = db.session.query(
        LedgerPayments.person_id,
        db.func.sum(LedgerPayments.amount).label('total_payments')
    ).group_by(LedgerPayments.person_id).subquery()

    return (
        db.session.query(
            People.id,
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            (charges_subquery.c.total_charges - db.func.coalesce(
                payments_subquery.c.total_payments, 0)).label("outstanding_balance"),
        )
        .join(charges_subquery, People.id == charges_subquery.c.person_id)
        .outerjoin(payments_subquery, People.id == payments_subquery.c.person_id)
        .filter(charges_subquery.c.total_charges > db.func.coalesce(payments_subquery.c.total_payments, 0))
        .filter(charges_subquery.c.practice_id == practice_id)
        .all()
    )

"""
Billing > Views - This file contains the routes for the billing blueprint.
"""

# Imports
import json
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.billing.forms import AddLedgerChargeForm, AddLedgerPaymentForm
from src import db
from src.models import People, Charges
from src.models import LedgerCharges, LedgerPayments, Notes


# Blueprint configuration
billing = Blueprint("billing", __name__)


# Billing
@billing.route("/billing")
@login_required
def ledger():
    """Routes the user to the Billing page"""
    people = People.query.filter_by(practice_id=current_user.practice_id).all()
    ledger_charges = (
        db.session.query(
            LedgerCharges.created_at,
            LedgerCharges.units,
            LedgerCharges.unit_amount,
            LedgerCharges.tax_rate,
            LedgerCharges.practice_id,
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
        .filter_by(practice_id=current_user.practice_id)
        .all()
    )
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0
    return render_template(
        "billing/billing.html",
        title="Soulstone - Billing",
        user=current_user,
        people=people,
        ledger_charges=ledger_charges,
        total_charges=total_charges,
        total_payments=total_payments,
    )


# Billing - Balance
@billing.route("/billing/balance")
@login_required
def balance():
    """Routes the user to the Balance page"""
    # queries
    people = People.query.filter_by(practice_id=current_user.practice_id).all()
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0

    # List of outstanding balances
    balances = (
        People.query.join(LedgerCharges)
        .join(LedgerPayments)
        .filter(
            People.practice_id == current_user.practice_id,
            LedgerCharges.unit_amount > LedgerPayments.amount,
        )
        .all()
    )

    return render_template(
        "billing/balance.html",
        title="Soulstone - Balance",
        user=current_user,
        people=people,
        total_charges=total_charges,
        total_payments=total_payments,
        balances=balances,
    )


# Billing - Add Ledger Charge
@billing.route("/billing/<int:id>/add_ledger_charge", methods=["GET", "POST"])
@login_required
def addLedgerCharge(id):
    """Routes the user to the add new ledger charge page"""
    form = AddLedgerChargeForm()

    pers_id = People.query.get_or_404(id).id
    practice_charges = Charges.query.filter_by(
        practice_id=current_user.practice_id
    ).all()

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = People.query.get_or_404(id).practice_id
    notes_count = Notes.query.filter_by(person_id=id).count()
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id, person_id=id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id, person_id=id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0
    balance = total_charges - total_payments

    if request.method == "GET":
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            # List of charges for the select field
            form.charge_id.choices = [
                (str(charge.id), charge.description +
                 f' (${charge.amount:.2f})')
                for charge in practice_charges
            ]

            return render_template(
                "billing/add_ledger_charge.html",
                title="Soulstone - Add New Charge",
                user=current_user,
                person=person,
                notes_count=notes_count,
                practice_charges=practice_charges,
                form=form,
                balance=balance,
            )
        else:
            return render_template("error_pages/401.html", user=current_user)

    if form.validate_on_submit and request.method == "POST":
        practice_id = current_user.practice_id
        charge_id = form.charge_id.data
        person_id = pers_id
        created_at = datetime.utcnow()
        created_by = current_user.get_id()
        updated_at = datetime.utcnow()
        updated_by = current_user.get_id()
        units = form.units.data
        unit_amount = form.unit_amount.data
        tax_rate_form = form.tax_rate.data
        if tax_rate_form:
            tax_rate = tax_rate_form / 100
        else:
            tax_rate = 0

        # Add new ledger charge to the database
        new_ledger_charge = LedgerCharges(
            practice_id=practice_id,
            charge_id=charge_id,
            person_id=person_id,
            # note_id=note_id,
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            units=units,
            unit_amount=unit_amount,
            tax_rate=tax_rate,
        )
        db.session.add(new_ledger_charge)
        db.session.commit()
        flash("Charge added successfully.", category="success")

        return redirect(url_for("billing.ledger"))

    return render_template(
        "billing/add_ledger_charge.html",
        title="Soulstone - Add Charge",
        user=current_user,
        form=form,
    )


# Payments
@billing.route("/billing/payments")
@login_required
def payments():
    """Routes the user to the Billing > Payments page"""
    # queries
    people = People.query.filter_by(practice_id=current_user.practice_id).all()
    ledger_payments = (
        db.session.query(
            LedgerPayments.created_at,
            LedgerPayments.payment_method,
            LedgerPayments.amount,
            LedgerPayments.payment_note,
            LedgerPayments.practice_id,
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            People.gender_identity,
        )
        .join(People, LedgerPayments.person_id == People.id)
        .filter_by(practice_id=current_user.practice_id)
        .all()
    )
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0

    return render_template(
        "billing/payments.html",
        title="Soulstone - Payments",
        user=current_user,
        people=people,
        ledger_payments=ledger_payments,
        total_charges=total_charges,
        total_payments=total_payments,
    )


@billing.route("/billing/payments/<int:id>/add_payment",
               methods=["GET", "POST"])
@login_required
def addLedgerPayment(id):
    """Routes the user to the add new ledger payment page"""
    form = AddLedgerPaymentForm()

    pers_id = People.query.get_or_404(id).id
    practice_charges = Charges.query.filter_by(
        practice_id=current_user.practice_id
    ).all()

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = People.query.get_or_404(id).practice_id
    notes_count = Notes.query.filter_by(person_id=id).count()
    total_charges = (
        db.session.query(
            db.func.sum(
                LedgerCharges.units * LedgerCharges.unit_amount
                + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)
            )
        )
        .filter_by(practice_id=current_user.practice_id, person_id=id)
        .scalar()
    )
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id, person_id=id)
        .scalar()
    )

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0
    balance = total_charges - total_payments

    if request.method == "GET":
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            return render_template(
                "billing/add_ledger_payment.html",
                title="Soulstone - Add New Payment",
                user=current_user,
                person=person,
                notes_count=notes_count,
                practice_charges=practice_charges,
                form=form,
                balance=balance,
            )
        else:
            return render_template("error_pages/401.html", user=current_user)

    if form.validate_on_submit and request.method == "POST":
        practice_id = current_user.practice_id
        person_id = pers_id
        created_at = datetime.utcnow()
        created_by = current_user.get_id()
        updated_at = datetime.utcnow()
        updated_by = current_user.get_id()
        payment_method = form.payment_method.data
        payment_amount = form.payment_amount.data
        check_number = form.check_number.data
        credit_card_number = form.credit_card_number.data
        payment_note = form.payment_note.data

        # Add new ledger charge to the database
        new_ledger_payment = LedgerPayments(
            practice_id=practice_id,
            person_id=person_id,
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            payment_method=payment_method,
            amount=payment_amount,
            check_number=check_number,
            credit_card_last_four=credit_card_number,
            payment_note=payment_note,
        )
        db.session.add(new_ledger_payment)
        db.session.commit()
        flash("Payment added successfully.", category="success")

        return redirect(url_for("billing.payments"))

    return render_template(
        "billing/add_ledger_payment.html",
        title="Soulstone - Add Payment",
        user=current_user,
        form=form,
    )

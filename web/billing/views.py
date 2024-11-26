"""Billing > Views - Routes for the billing blueprint."""
# Imports
import pdfkit
from datetime import datetime, timedelta, timezone
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for,
    make_response)
from flask_login import login_required, current_user
from persons.models import People
from settings.models import Practice
from persons.person_header import personHeader
from app import db
from .models import Charges, LedgerCharges, LedgerPayments
from .forms import AddLedgerChargeForm, AddLedgerPaymentForm
from .controls import (
    get_people, get_ledger_charges, get_total_charges, get_total_payments,
    get_outstanding_balances)


# Blueprint configuration
billing = Blueprint("billing", __name__)


# Billing
@billing.route("/billing/charges")
@login_required
def ledger():
    """Routes the user to the Billing page"""

    start_date = datetime.now(tz=timezone.utc) - timedelta(days=120)
    people = get_people(current_user.practice_id)
    ledger_charges = get_ledger_charges(current_user.practice_id, start_date)
    total_charges = get_total_charges(current_user.practice_id) or 0
    total_payments = get_total_payments(current_user.practice_id) or 0

    return render_template(
        "billing/billing.html", title="Soulstone - Billing", people=people,
        ledger_charges=ledger_charges, total_charges=total_charges,
        total_payments=total_payments)


# Billing - Balance
@billing.route("/billing/balance")
@login_required
def balance():
    """Routes the user to the Balance page"""

    people = get_people(current_user.practice_id)
    total_charges = get_total_charges(current_user.practice_id) or 0
    total_payments = get_total_payments(current_user.practice_id) or 0
    balances = get_outstanding_balances(current_user.practice_id)

    return render_template(
        "billing/balance.html", title="Soulstone - Balance", user=current_user,
        people=people, total_charges=total_charges,
        total_payments=total_payments, balances=balances)


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

    if request.method == "GET":
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            # Base Person Header
            person_header, notes_count, events_count, balance = personHeader(
                id)

            # List of charges for the select field
            form.charge_id.choices = [
                (str(charge.id), charge.description +
                 f" (${charge.amount:.2f})" +
                 f" ({charge.tax_rate}%)")
                for charge in practice_charges
            ]

            return render_template(
                "billing/add_ledger_charge.html",
                title="Soulstone - Add New Charge",
                user=current_user,
                person=person,
                practice_charges=practice_charges,
                form=form,
                person_header=person_header,
                notes_count=notes_count,
                events_count=events_count,
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


# Billing - Ledger Charge - View
@billing.route("/billing/ledger_charge/<int:ledger_charge_id>")
@login_required
def view_ledger_charge(ledger_charge_id):
    """View a ledger charge"""

    # queries
    ledger_charge = LedgerCharges.query.get_or_404(ledger_charge_id)
    person = People.query.get_or_404(ledger_charge.person_id)
    charge = Charges.query.get_or_404(ledger_charge.charge_id)

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = person.practice_id

    # check if user practice id matches patient user id
    if pu_id == pp_id:
        # Base Person Header
        person_header, notes_count, events_count, balance = personHeader(
            person.id)

        return render_template(
            "billing/view_ledger_charge.html",
            title="Soulstone - Ledger Charge",
            user=current_user,
            ledger_charge=ledger_charge,
            person=person,
            charge=charge,
            person_header=person_header,
            notes_count=notes_count,
            events_count=events_count,
            balance=balance,
        )
    else:
        return render_template("error_pages/401.html", user=current_user)


# Billing - Ledger Charge - Delete
@billing.route("/billing/ledger_charge/<int:ledger_charge_id>/delete",
               methods=["POST"])
@login_required
def delete_ledger_charge(ledger_charge_id):
    """Delete a ledger charge"""

    # queries
    ledger_charge = LedgerCharges.query.get_or_404(ledger_charge_id)

    # Delete the ledger charge
    if request.method == "POST":
        db.session.delete(ledger_charge)
        db.session.commit()
        flash("Ledger charge deleted successfully.", category="success")
        return redirect(url_for("billing.ledger"))


# Payments
@billing.route("/billing/payments")
@login_required
def payments():
    """Routes the user to the Billing > Payments page"""

    start_date = datetime.utcnow() - timedelta(days=120)

    people = People.query.filter_by(practice_id=current_user.practice_id).all()
    ledger_payments = (
        db.session.query(
            LedgerPayments.id,
            LedgerPayments.created_at,
            LedgerPayments.payment_method,
            LedgerPayments.amount,
            LedgerPayments.payment_note,
            LedgerPayments.practice_id,
            People.id.label("person_id"),
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            People.gender_identity,
        )
        .join(People, LedgerPayments.person_id == People.id)
        .filter(LedgerPayments.practice_id == current_user.practice_id,
                LedgerPayments.created_at >= start_date)
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

    if request.method == "GET":
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            # Base Person Header
            person_header, notes_count, events_count, balance = personHeader(
                id)

            return render_template(
                "billing/add_ledger_payment.html",
                title="Soulstone - Add New Payment",
                user=current_user,
                person=person,
                practice_charges=practice_charges,
                form=form,
                person_header=person_header,
                notes_count=notes_count,
                events_count=events_count,
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


# Billing - Ledger Payment - View
@billing.route("/billing/ledger_payment/<int:ledger_payment_id>")
@login_required
def view_ledger_payment(ledger_payment_id):
    """View the ledger payment"""

    # queries
    ledger_payment = LedgerPayments.query.get_or_404(ledger_payment_id)
    person = People.query.get_or_404(ledger_payment.person_id)

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = person.practice_id

    # check if user practice id matches patient user id
    if pu_id == pp_id:
        # Base Person Header
        person_header, notes_count, events_count, balance = personHeader(
            person.id)

        return render_template(
            "billing/view_ledger_payment.html",
            title="Soulstone - Ledger Payment",
            user=current_user,
            ledger_payment=ledger_payment,
            person=person,
            person_header=person_header,
            notes_count=notes_count,
            events_count=events_count,
            balance=balance,
        )
    else:
        return render_template("error_pages/401.html", user=current_user)


# Billing - Ledger Payment - Delete
@billing.route(
    "/billing/ledger_payment/<int:ledger_payment_id>/delete", methods=["POST"]
)
@login_required
def delete_ledger_payment(ledger_payment_id):
    """Delete a ledger payment"""

    # queries
    ledger_payment = LedgerPayments.query.get_or_404(ledger_payment_id)

    # Delete the ledger charge
    if request.method == "POST":
        db.session.delete(ledger_payment)
        db.session.commit()
        flash("Ledger payment deleted successfully.", category="success")
        return redirect(url_for("billing.payments"))


# Generate Invoice for Person
@billing.route("/billing/invoices/<int:person_id>/generate_invoice")
@login_required
def generateInvoice(person_id):
    """Generates an invoice for the person"""

    # Current Date
    current_date = datetime.utcnow()

    # Ledger Charges
    ledger_charges = (
        db.session.query(
            LedgerCharges.created_at,
            LedgerCharges.charge_id,
            LedgerCharges.units,
            LedgerCharges.unit_amount,
            LedgerCharges.tax_rate,
            LedgerCharges.practice_id,
            LedgerCharges.person_id,
            Charges.id,
            Charges.name,
            Charges.description,
        )
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .outerjoin(Charges, Charges.id == LedgerCharges.charge_id)
        .order_by(LedgerCharges.created_at.desc())
        .all()
    )

    # Ledger Payments
    ledger_payments = (
        db.session.query(
            LedgerPayments.created_at,
            LedgerPayments.payment_method,
            LedgerPayments.amount,
            LedgerPayments.payment_note,
            LedgerPayments.practice_id,
            LedgerPayments.person_id,
        )
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .order_by(LedgerPayments.created_at.desc())
        .all()
    )

    # Person
    person = People.query.get_or_404(person_id)

    # Practice
    practice = Practice.query.get_or_404(current_user.practice_id)

    # Total Charges
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

    # Total Payments
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .scalar()
    )

    # Base Person Header
    person_header, notes_count, events_count, balance = personHeader(person_id)

    # Render the invoice
    return render_template(
        "billing/invoice.html",
        title="Soulstone - Invoice",
        user=current_user,
        current_date=current_date,
        ledger_charges=ledger_charges,
        ledger_payments=ledger_payments,
        person=person,
        practice=practice,
        total_charges=total_charges,
        total_payments=total_payments,
        person_header=person_header,
        notes_count=notes_count,
        events_count=events_count,
        balance=balance,
    )


# Billing - Invoice - Print Invoice
@billing.route("/billing/invoices/<int:person_id>/print_invoice")
@login_required
def pdfInvoice(person_id):
    """Prints the invoice for a person"""

    # Current Date
    current_date = datetime.utcnow()

    # Ledger Charges
    ledger_charges = (
        db.session.query(
            LedgerCharges.created_at,
            LedgerCharges.charge_id,
            LedgerCharges.units,
            LedgerCharges.unit_amount,
            LedgerCharges.tax_rate,
            LedgerCharges.practice_id,
            LedgerCharges.person_id,
            Charges.id,
            Charges.name,
            Charges.description,
        )
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .outerjoin(Charges, Charges.id == LedgerCharges.charge_id)
        .order_by(LedgerCharges.created_at.desc())
        .all()
    )

    # Ledger Payments
    ledger_payments = (
        db.session.query(
            LedgerPayments.created_at,
            LedgerPayments.payment_method,
            LedgerPayments.amount,
            LedgerPayments.payment_note,
            LedgerPayments.practice_id,
            LedgerPayments.person_id,
        )
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .order_by(LedgerPayments.created_at.desc())
        .all()
    )

    # Person
    person = People.query.get_or_404(person_id)

    # Practice
    practice = Practice.query.get_or_404(current_user.practice_id)

    # Total Charges
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

    # Total Payments
    total_payments = (
        db.session.query(db.func.sum(LedgerPayments.amount))
        .filter_by(practice_id=current_user.practice_id, person_id=person_id)
        .scalar()
    )

    # Balance
    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0

    balance = total_charges - total_payments

    # Create PDF
    rendered = render_template(
        "billing/pdf_invoice.html",
        title=f"Soulstone - {person.first_name} {person.last_name} Invoice",
        current_date=current_date,
        ledger_charges=ledger_charges,
        ledger_payments=ledger_payments,
        balance=balance,
        practice=practice,
        person=person,
        user=current_user,
    )
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers[
        "Content-Disposition"
    ] = f"inline;\
        filename={person.first_name}_{person.last_name}_invoice_{current_date}.pdf"
    return response


# Billing - Payments - Print Receipt
@billing.route("/billing/payments/<int:payment_id>/print_receipt")
@login_required
def pdfPaymentReceipt(payment_id):
    """Prints the payment receipt"""

    payment = LedgerPayments.query.get_or_404(payment_id)
    practice = Practice.query.filter_by(id=payment.practice_id).first()
    person = People.query.filter_by(id=payment.person_id).first()

    rendered = render_template(
        "billing/pdf_payment_receipt.html",
        payment=payment,
        practice=practice,
        person=person,
        user=current_user,
    )
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;\
        filename=payment_receipt.pdf"
    return response

"""
Dashboard - Views -- This file contains the views for the dashboard app.
"""


# Imports
from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from persons.models import People
from events.models import Events
from visit_notes.models import Notes
from billing.models import LedgerCharges, LedgerPayments


# Blueprint Configuration
dashboard = Blueprint("dashboard", __name__)


# Dashboard
@dashboard.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    """Route for the dashboard."""

    # Start Date for Dashboard (120 days)
    start_date = datetime.now() - timedelta(days=120)

    # Dashboard - Newly Created Persons
    person_data = (
        db.session.query(
            db.func.count(People.id).label("count"),
            db.func.strftime("%Y-%m", People.created_at).label("month"),
        )
        .filter(
            People.practice_id == current_user.practice_id,
            People.created_at >= start_date,
        )
        .group_by("month")
        .all()
    )

    person_graph_labels = [person.month for person in person_data]
    person_graph_data = [person.count for person in person_data]

    # Dashboard - Events by Event Date
    events_data = (
        db.session.query(
            db.func.count(Events.id).label("count"),
            db.func.strftime("%Y-%m", Events.date).label("month"),
        )
        .filter(
            Events.practice_id == current_user.practice_id,
            Events.date >= start_date
        )
        .group_by("month")
        .all()
    )

    events_graph_labels = [event.month for event in events_data]
    events_graph_data = [event.count for event in events_data]

    # Dashboard - Ledger Charges
    ledger_charges_data = (
        db.session.query(
            db.func.sum(
                LedgerCharges.unit_amount
                * LedgerCharges.units
                * (1 + LedgerCharges.tax_rate)
            ).label("sum"),
            db.func.strftime("%Y-%m", LedgerCharges.created_at).label("month"),
        )
        .filter(
            LedgerCharges.practice_id == current_user.practice_id,
            LedgerCharges.created_at >= start_date,
        )
        .group_by("month")
        .all()
    )

    ledger_charges_graph_labels = [
        charge.month for charge in ledger_charges_data]
    ledger_charges_graph_data = [charge.sum for charge in ledger_charges_data]

    ledger_charges_graph_labels = [
        charge.month for charge in ledger_charges_data]
    ledger_charges_graph_data = [charge.sum for charge in ledger_charges_data]

    # Dashboard - Ledger Payments
    ledger_payments_data = (
        db.session.query(
            db.func.sum(LedgerPayments.amount).label("sum"),
            db.func.strftime(
                "%Y-%m", LedgerPayments.created_at).label("month"),
        )
        .filter(
            LedgerPayments.practice_id == current_user.practice_id,
            LedgerPayments.created_at >= start_date,
        )
        .group_by("month")
        .all()
    )

    ledger_payments_graph_labels = [
        payment.month for payment in ledger_payments_data]
    ledger_payments_graph_data = [
        payment.sum for payment in ledger_payments_data]

    # Dashboard - Visit Notes by Date of Service
    visit_notes_data = (
        db.session.query(
            db.func.count(Notes.id).label("count"),
            db.func.strftime("%Y-%m", Notes.date_of_service).label("month"),
        )
        .filter(
            Notes.practice_id == current_user.practice_id,
            Notes.date_of_service >= start_date,
        )
        .group_by("month")
        .all()
    )

    visit_notes_graph_labels = [note.month for note in visit_notes_data]
    visit_notes_graph_data = [note.count for note in visit_notes_data]

    return render_template(
        "dashboard/dashboard.html",
        title="Soulstone - Dashboard",
        user=current_user,
        person_graph_labels=person_graph_labels,
        person_graph_data=person_graph_data,
        events_graph_labels=events_graph_labels,
        events_graph_data=events_graph_data,
        visit_notes_graph_labels=visit_notes_graph_labels,
        visit_notes_graph_data=visit_notes_graph_data,
        ledger_charges_graph_labels=ledger_charges_graph_labels,
        ledger_charges_graph_data=ledger_charges_graph_data,
        ledger_payments_graph_labels=ledger_payments_graph_labels,
        ledger_payments_graph_data=ledger_payments_graph_data,
    )

"""
Reports - Views -- This file contains the views for the reports app.
"""


# Imports
import csv
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from src.reports.forms import GenerateReportForm
from src import db
from src.models import (
    User, People, Events, Notes, LedgerCharges, LedgerPayments,
    EventTypes,
)


# Blueprint Configuration
reports = Blueprint("reports", __name__)


# Reports
@reports.route("/reports", methods=["GET", "POST"])
@login_required
def generate_report():
    """Route for generating and viewing reports."""

    form = GenerateReportForm()

    # Report Options
    # Make sure to update the following functions:
    # - get_column_labels()
    # - generate_report_data()
    form.report_options.choices = [
        ("Person Report", "Person Report"),
        ("Event Report", "Event Report"),
        ("Open Visit Notes Report", "Open Visit Notes Report"),
    ]

    if request.method == "POST":
        # Get the selected report and date parameters from the form
        selected_report = form.report_options.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Generate report data based on the selected report and date parameters
        report_data = generate_report_data(
            selected_report, start_date, end_date)

        # Define custom column labels based on the selected report
        column_labels = get_column_labels(selected_report)

        # Render the report template with the generated data
        return render_template(
            "reports/report.html",
            title="Soulstone - Report",
            user=current_user,
            report_data=report_data,
            selected_report=selected_report,
            start_date=start_date,
            end_date=end_date,
            column_labels=column_labels,
        )

    return render_template(
        "reports/generate_report.html", title="Soulstone - Generate Report",
        form=form,
        user=current_user,
    )


def get_column_labels(report):
    """Get custom column labels based on the selected report."""

    if report == "Person Report":
        return [
            "First Name",
            "Middle Name",
            "Last Name",
            "Suffix",
            "Email",
            "Created At",
        ]
    elif report == "Event Report":
        return [
            "Event Name",
            "Event Date",
            "Event Start Time",
            "Event End Time",
            "Person ID",
            "Person First Name",
            "Person Last Name",
            "Practitioner First Name",
            "Practitioner Last Name",
            "Event Notes",
        ]
    # Open Visit Notes Report
    elif report == "Open Visit Notes Report":
        return [
            "Person ID",
            "Person First Name",
            "Person Middle Name",
            "Person Last Name",
            "Person Suffix",
            "Visit Note ID",
            "Visit Note Created Date",
            "Visit Note Status",
        ]
    else:
        # Handle other report options if needed
        return []


def generate_report_data(report, start_date, end_date):
    """
    Generate report data based on the selected report
    and date parameters.
    """

    if report == "Person Report":
        person_report_data = (
            db.session.query(
                People.first_name,
                People.middle_name,
                People.last_name,
                People.suffix_name,
                People.email,
                People.created_at,
            )
            .filter(
                People.practice_id == current_user.practice_id,
                People.created_at >= start_date,
                People.created_at <= end_date
            )
            .all()
        )

        return person_report_data
    elif report == "Event Report":
        event_report_data = (
            db.session.query(
                EventTypes.event_name,
                Events.date,
                Events.start_time,
                Events.end_time,
                People.id,
                People.first_name,
                People.last_name,
                User.first_name,
                User.last_name,
                Events.note,
            )
            .outerjoin(People, People.id == Events.person_id)
            .outerjoin(User, User.id == Events.practitioner_id)
            .join(EventTypes, EventTypes.id == Events.event_type_id)
            .filter(
                Events.practice_id == current_user.practice_id,
                Events.date >= start_date,
                Events.date <= end_date
            )
            .all()
        )

        return event_report_data
    # Open Visit Notes Report
    elif report == "Open Visit Notes Report":
        open_visit_notes_report_data = (
            db.session.query(
                People.id,
                People.first_name,
                People.middle_name,
                People.last_name,
                People.suffix_name,
                Notes.id,
                Notes.created_at,
                Notes.status,
            )
            .join(People, People.id == Notes.person_id)
            .filter(
                Notes.practice_id == current_user.practice_id,
                Notes.status == "Open",
                Notes.created_at >= start_date,
                Notes.created_at <= end_date,
            )
            .all()
        )

        return open_visit_notes_report_data
    else:
        # Handle other report options if needed
        return []

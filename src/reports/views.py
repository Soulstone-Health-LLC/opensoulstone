"""
Reports - Views -- This file contains the views for the reports app.
"""


# Imports
import csv
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from src.reports.forms import GenerateReportForm
from src import db
from src.models import People, Events, Notes, LedgerCharges, LedgerPayments


# Blueprint Configuration
reports = Blueprint("reports", __name__)


# Reports
@reports.route("/reports", methods=["GET", "POST"])
@login_required
def generate_report():
    """Route for generating and viewing reports."""

    form = GenerateReportForm()

    # Report Options
    form.report_options.choices = [
        ("person_report", "Person Report"),
        ("event_report", "Event Report"),
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

    # Render the form to generate reports
    return render_template(
        "reports/generate_report.html", title="Soulstone - Generate Report",
        form=form,
        user=current_user,
    )


def get_column_labels(report):
    """Get custom column labels based on the selected report."""

    if report == "person_report":
        return [
            "First Name",
            "Middle Name",
            "Last Name",
            "Suffix",
            "Email",
            "Created At",
        ]
    elif report == "event_report":
        return ["Event Name", "Event Date", "Location"]
    else:
        # Handle other report options if needed
        return []


def generate_report_data(report, start_date, end_date):
    """
    Generate report data based on the selected report
    and date parameters.
    """

    if report == "person_report":
        # Generate person report data using the provided start_date and end_date
        # Query the database based on the date parameters and return the data

        # Example query:
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
    elif report == "event_report":
        # Generate event report data using the provided start_date and end_date
        # Query the database based on the date parameters and return the data

        # Example query:
        event_report_data = (
            db.session.query(
                Events.name, Events.date, Events.location
            )
            .filter(
                Events.practice_id == current_user.practice_id,
                Events.date >= start_date,
                Events.date <= end_date
            )
            .all()
        )

        return event_report_data
    else:
        # Handle other report options if needed
        return []

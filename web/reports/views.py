from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user
from datetime import datetime
import csv
import io
from app import db
from users.models import User
from persons.models import People
from events.models import Events, EventTypes
from visit_notes.models import Notes
from billing.models import LedgerCharges, LedgerPayments
from reports.forms import GenerateReportForm

# Blueprint Configuration
reports = Blueprint("reports", __name__)


# Reports Landing Page
@reports.route("/reports", methods=["GET"])
@login_required
def reports_landing():
    """Route for the reports landing page."""
    return render_template("reports/reports_landing.html", title="Soulstone - Reports", user=current_user)


# Person Report
@reports.route("/reports/person", methods=["GET", "POST"])
@login_required
def person_report():
    """Route for generating and viewing the Person Report."""
    form = GenerateReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        report_data = generate_person_report_data(start_date, end_date)
        column_labels = get_column_labels("Person Report")
        return render_template("reports/report.html", title="Soulstone - Person Report", form=form, user=current_user, report_data=report_data, column_labels=column_labels, start_date=start_date, end_date=end_date, selected_report="Person Report")
    return render_template("reports/generate_report.html", title="Soulstone - Generate Person Report", form=form, user=current_user)


# Birthday Report
@reports.route("/reports/birthday", methods=["GET", "POST"])
@login_required
def birthday_report():
    """Route for generating and viewing the Birthday Report."""
    form = GenerateReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        report_data = generate_birthday_report_data(start_date, end_date)
        column_labels = get_column_labels("Birthday Report")
        return render_template("reports/report.html", title="Soulstone - Birthday Report", form=form, user=current_user, report_data=report_data, column_labels=column_labels, start_date=start_date, end_date=end_date, selected_report="Birthday Report")
    return render_template("reports/generate_report.html", title="Soulstone - Generate Birthday Report", form=form, user=current_user)


# Event Report
@reports.route("/reports/event", methods=["GET", "POST"])
@login_required
def event_report():
    """Route for generating and viewing the Event Report."""
    form = GenerateReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        report_data = generate_event_report_data(start_date, end_date)
        column_labels = get_column_labels("Event Report")
        return render_template("reports/report.html", title="Soulstone - Event Report", form=form, user=current_user, report_data=report_data, column_labels=column_labels, start_date=start_date, end_date=end_date, selected_report="Event Report")
    return render_template("reports/generate_report.html", title="Soulstone - Generate Event Report", form=form, user=current_user)


# Open Visit Notes Report
@reports.route("/reports/open-visit-notes", methods=["GET", "POST"])
@login_required
def open_visit_notes_report():
    """Route for generating and viewing the Open Visit Notes Report."""
    form = GenerateReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        report_data = generate_open_visit_notes_report_data(
            start_date, end_date)
        column_labels = get_column_labels("Open Visit Notes Report")
        return render_template("reports/report.html", title="Soulstone - Open Visit Notes Report", form=form, user=current_user, report_data=report_data, column_labels=column_labels, start_date=start_date, end_date=end_date, selected_report="Open Visit Notes Report")
    return render_template("reports/generate_report.html", title="Soulstone - Generate Open Visit Notes Report", form=form, user=current_user)


# Open Balances Report
@reports.route("/reports/open-balances", methods=["GET", "POST"])
@login_required
def open_balances_report():
    """Route for generating and viewing the Open Balances Report."""
    form = GenerateReportForm()
    if form.validate_on_submit():
        report_data = generate_open_balances_report_data()
        column_labels = get_column_labels("Open Balances Report")
        return render_template("reports/report.html", title="Soulstone - Open Balances Report", form=form, user=current_user, report_data=report_data, column_labels=column_labels, selected_report="Open Balances Report")
    return render_template("reports/generate_report.html", title="Soulstone - Generate Open Balances Report", form=form, user=current_user)


# Export CSV
@reports.route("/reports/export-csv", methods=["POST"])
@login_required
def export_csv():
    """Route for exporting report data as CSV."""
    current_time = datetime.utcnow()
    selected_report = request.form.get("selected_report")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    report_data = generate_report_data(selected_report, start_date, end_date)
    column_labels = get_column_labels(selected_report)
    csv_output = generate_csv(report_data, column_labels)
    response = make_response(csv_output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={
        selected_report}_{current_time}.csv"
    response.headers["Content-type"] = "text/csv"
    return response


# Helper Functions
def generate_csv(data, column_labels):
    """Generate a CSV file from the provided data and column labels."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(column_labels)
    for row in data:
        writer.writerow(row)
    return output


def get_column_labels(report):
    """Get custom column labels based on the selected report."""
    if report == "Person Report":
        return ["First Name", "Middle Name", "Last Name", "Suffix", "Email", "Created At"]
    elif report == "Event Report":
        return ["Event Name", "Event Date", "Event Start Time", "Event End Time", "Person ID", "Person First Name", "Person Last Name", "Practitioner First Name", "Practitioner Last Name", "Event Notes"]
    elif report == "Open Visit Notes Report":
        return ["Person ID", "Person First Name", "Person Middle Name", "Person Last Name", "Person Suffix", "Visit Note ID", "Visit Note Created Date", "Visit Note Status"]
    elif report == "Birthday Report":
        return ["Person ID", "Person First Name", "Person Middle Name", "Person Last Name", "Person Suffix", "Date of Birth"]
    elif report == "Open Balances Report":
        return ["Person ID", "Person First Name", "Person Last Name", "Balance"]
    else:
        return []


def generate_report_data(report, start_date, end_date):
    """Generate report data based on the selected report and date parameters."""
    if report == "Person Report":
        return generate_person_report_data(start_date, end_date)
    elif report == "Event Report":
        return generate_event_report_data(start_date, end_date)
    elif report == "Open Visit Notes Report":
        return generate_open_visit_notes_report_data(start_date, end_date)
    elif report == "Birthday Report":
        return generate_birthday_report_data(start_date, end_date)
    elif report == "Open Balances Report":
        return generate_open_balances_report_data()
    else:
        return []


def generate_person_report_data(start_date, end_date):
    """Generate data for the Person Report."""
    return db.session.query(People.first_name, People.middle_name, People.last_name, People.suffix_name, People.email, People.created_at).filter(People.practice_id == current_user.practice_id, People.created_at >= start_date, People.created_at <= end_date).all()


def generate_event_report_data(start_date, end_date):
    """Generate data for the Event Report."""
    return db.session.query(EventTypes.event_name, Events.date, Events.start_time, Events.end_time, People.id, People.first_name, People.last_name, User.first_name, User.last_name, Events.note).outerjoin(People, People.id == Events.person_id).outerjoin(User, User.id == Events.practitioner_id).join(EventTypes, EventTypes.id == Events.event_type_id).filter(Events.practice_id == current_user.practice_id, Events.date >= start_date, Events.date <= end_date).all()


def generate_open_visit_notes_report_data(start_date, end_date):
    """Generate data for the Open Visit Notes Report."""
    return db.session.query(People.id, People.first_name, People.middle_name, People.last_name, People.suffix_name, Notes.id, Notes.created_at, Notes.status).join(People, People.id == Notes.person_id).filter(Notes.practice_id == current_user.practice_id, Notes.status == "Open", Notes.created_at >= start_date, Notes.created_at <= end_date).all()


def generate_birthday_report_data(start_date, end_date):
    """Generate data for the Birthday Report."""
    return db.session.query(People.id, People.first_name, People.middle_name, People.last_name, People.suffix_name, People.date_of_birth).filter(People.practice_id == current_user.practice_id, People.date_of_birth >= start_date, People.date_of_birth <= end_date).all()


def generate_open_balances_report_data():
    """Generate data for the Open Balances Report."""
    return db.session.query(People.id, People.first_name, People.last_name, db.func.coalesce(db.func.sum(LedgerCharges.unit_amount * LedgerCharges.units + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)) - db.func.coalesce(db.func.sum(LedgerPayments.amount), 0), 0).label("balance")).outerjoin(LedgerCharges).outerjoin(LedgerPayments).group_by(People.id, People.first_name, People.last_name).having(db.func.coalesce(db.func.sum(LedgerCharges.unit_amount * LedgerCharges.units + (LedgerCharges.unit_amount * LedgerCharges.tax_rate)), 0) > db.func.coalesce(db.func.sum(LedgerPayments.amount), 0)).filter(People.practice_id == current_user.practice_id).all()

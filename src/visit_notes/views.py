"""
Visit Nots > Views - This file contains the views for the Visit Notes
Blueprint.
"""


# Imports
import pdfkit
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import make_response
from flask_login import login_required, current_user
from src.visit_notes.forms import (
    AddVisitNoteForm,
    EditVisitNoteForm,
    ChangeVisitNoteStatusForm,
    DeleteVisitNoteForm,
)
from src import db
from src.models import People, Practice, Notes
from src.persons.person_header import personHeader


# Blueprint Configuration
visit_notes = Blueprint("visit_notes", __name__)


# Routes - Practice - Notes
@visit_notes.route("/notes")
@login_required
def notes():
    """Routes the user to the Notes page"""
    visit_notes = (
        db.session.query(
            Notes.id,
            Notes.date_of_service,
            Notes.status,
            Notes.practice_id,
            People.id.label("person_id"),
            People.first_name,
            People.middle_name,
            People.last_name,
            People.suffix_name,
            People.gender_identity,
        )
        .filter_by(practice_id=current_user.practice_id)
        .join(People, Notes.person_id == People.id)
        .all()
    )

    people = People.query.filter_by(practice_id=current_user.practice_id).all()

    return render_template(
        "visit_notes/notes.html",
        title="Soulstone - Notes",
        user=current_user,
        visit_notes=visit_notes,
        people=people,
    )


# Add Visit Note
@visit_notes.route("/notes/<int:id>/add_visit_note", methods=["GET", "POST"])
@login_required
def addVisitNote(id):
    """Add a new visit note to the database"""

    form = AddVisitNoteForm()

    pers_id = People.query.get_or_404(id).id

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

            # Chart - Chakra Assessment
            # Start Date for Dashboard (365 days)
            start_date = datetime.now() - timedelta(days=365)
            chakra_data = (
                db.session.query(
                    db.func.strftime(
                        "%Y-%m-%d", Notes.date_of_service).label("day"),
                    Notes.chakra_assessment_root_score,
                    Notes.chakra_assessment_sacral_score,
                    Notes.chakra_assessment_solar_plexus_score,
                    Notes.chakra_assessment_heart_score,
                    Notes.chakra_assessment_throat_score,
                    Notes.chakra_assessment_third_eye_score,
                    Notes.chakra_assessment_crown_score,
                )
                .filter(
                    Notes.person_id == pers_id,
                    Notes.date_of_service >= start_date,
                )
                .group_by("day")
                .all()
            )

            chakra_graph_labels = [chakra.day for chakra in chakra_data]
            chakra_graph_data = [
                {
                    "Root Score": chakra.chakra_assessment_root_score,
                    "Sacral Score": chakra.chakra_assessment_sacral_score,
                    "Solar Plexus Score":
                        chakra.chakra_assessment_solar_plexus_score,
                    "Heart Score": chakra.chakra_assessment_heart_score,
                    "Throat Score": chakra.chakra_assessment_throat_score,
                    "Third Eye Score":
                        chakra.chakra_assessment_third_eye_score,
                    "Crown Score": chakra.chakra_assessment_crown_score,
                }
                for chakra in chakra_data
            ]

            return render_template(
                "visit_notes/add_visit_note.html",
                title="Soulstone - Add Visit Note",
                user=current_user,
                person=person,
                form=form,
                person_header=person_header,
                notes_count=notes_count,
                events_count=events_count,
                balance=balance,
                chakra_graph_labels=chakra_graph_labels,
                chakra_graph_data=chakra_graph_data,
            )
        else:
            return render_template("error_pages/401.html", user=current_user)

    if form.validate_on_submit() and request.method == "POST":
        # Get data from the form
        practice_id = current_user.practice_id
        person_id = pers_id
        created_at = datetime.utcnow()
        created_by = current_user.get_id()
        updated_at = datetime.utcnow()
        updated_by = current_user.get_id()
        date_of_service = form.date_of_service.data
        reason_for_visit = form.reason_for_visit.data
        chakra_assessment_root_score = form.chakra_assessment_root_score.data
        chakra_assessment_root_description = (
            form.chakra_assessment_root_description.data
        )
        chakra_assessment_sacral_score =\
            form.chakra_assessment_sacral_score.data
        chakra_assessment_sacral_description = (
            form.chakra_assessment_sacral_description.data
        )
        chakra_assessment_solar_plexus_score = (
            form.chakra_assessment_solar_plexus_score.data
        )
        chakra_assessment_solar_plexus_description = (
            form.chakra_assessment_solar_plexus_description.data
        )
        chakra_assessment_heart_score = form.chakra_assessment_heart_score.data
        chakra_assessment_heart_description = (
            form.chakra_assessment_heart_description.data
        )
        chakra_assessment_throat_score =\
            form.chakra_assessment_throat_score.data
        chakra_assessment_throat_description = (
            form.chakra_assessment_throat_description.data
        )
        chakra_assessment_third_eye_score =\
            form.chakra_assessment_third_eye_score.data
        chakra_assessment_third_eye_description = (
            form.chakra_assessment_third_eye_description.data
        )
        chakra_assessment_crown_score = form.chakra_assessment_crown_score.data
        chakra_assessment_crown_description = (
            form.chakra_assessment_crown_description.data
        )
        visit_notes = form.visit_notes.data
        post_visit_recommendations = form.post_visit_recommendations.data

        # Add new visit note to database
        new_visit_note = Notes(
            practice_id=practice_id,
            person_id=person_id,
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            date_of_service=date_of_service,
            reason_for_visit=reason_for_visit,
            chakra_assessment_root_score=chakra_assessment_root_score,
            chakra_assessment_root_description=(
                chakra_assessment_root_description),
            chakra_assessment_sacral_score=chakra_assessment_sacral_score,
            chakra_assessment_sacral_description=(
                chakra_assessment_sacral_description),
            chakra_assessment_solar_plexus_score=(
                chakra_assessment_solar_plexus_score),
            chakra_assessment_solar_plexus_description=(
                chakra_assessment_solar_plexus_description
            ),
            chakra_assessment_heart_score=chakra_assessment_heart_score,
            chakra_assessment_heart_description=(
                chakra_assessment_heart_description),
            chakra_assessment_throat_score=chakra_assessment_throat_score,
            chakra_assessment_throat_description=(
                chakra_assessment_throat_description),
            chakra_assessment_third_eye_score=(
                chakra_assessment_third_eye_score),
            chakra_assessment_third_eye_description=(
                chakra_assessment_third_eye_description
            ),
            chakra_assessment_crown_score=chakra_assessment_crown_score,
            chakra_assessment_crown_description=(
                chakra_assessment_crown_description),
            visit_notes=visit_notes,
            post_visit_recommendations=post_visit_recommendations,
        )
        db.session.add(new_visit_note)
        db.session.commit()
        flash("Visit Note created successfully.", category="success")

        # Redirect to Visit Notes page
        return redirect(url_for("visit_notes.notes"))


@visit_notes.route("/notes/<int:id>", methods=["GET", "POST"])
@login_required
def editVisitNote(id):
    form = EditVisitNoteForm()

    note = Notes.query.get_or_404(id)
    pers_id = note.person_id
    person = People.query.get_or_404(pers_id)

    if request.method == "GET":
        # Base Person Header
        person_header, notes_count, events_count, balance = personHeader(
            pers_id)

        # Chart - Chakra Assessment
        # Start Date for Dashboard (365 days)
        start_date = datetime.now() - timedelta(days=365)
        chakra_data = (
            db.session.query(
                db.func.strftime(
                    "%Y-%m-%d", Notes.date_of_service).label("day"),
                Notes.chakra_assessment_root_score,
                Notes.chakra_assessment_sacral_score,
                Notes.chakra_assessment_solar_plexus_score,
                Notes.chakra_assessment_heart_score,
                Notes.chakra_assessment_throat_score,
                Notes.chakra_assessment_third_eye_score,
                Notes.chakra_assessment_crown_score,
            )
            .filter(
                Notes.person_id == pers_id,
                Notes.date_of_service >= start_date,
            )
            .group_by("day")
            .all()
        )

        chakra_graph_labels = [chakra.day for chakra in chakra_data]
        chakra_graph_data = [
            {
                "Root Score": chakra.chakra_assessment_root_score,
                "Sacral Score": chakra.chakra_assessment_sacral_score,
                "Solar Plexus Score":
                chakra.chakra_assessment_solar_plexus_score,
                "Heart Score": chakra.chakra_assessment_heart_score,
                "Throat Score": chakra.chakra_assessment_throat_score,
                "Third Eye Score": chakra.chakra_assessment_third_eye_score,
                "Crown Score": chakra.chakra_assessment_crown_score,
            }
            for chakra in chakra_data
        ]

        # Populate form fields with existing data from database
        form.reason_for_visit.data = note.reason_for_visit
        form.date_of_service.data = note.date_of_service
        form.chakra_assessment_root_score.data = str(
            note.chakra_assessment_root_score)
        form.chakra_assessment_root_description.data = (
            note.chakra_assessment_root_description
        )
        form.chakra_assessment_sacral_score.data = str(
            note.chakra_assessment_sacral_score
        )
        form.chakra_assessment_sacral_description.data = (
            note.chakra_assessment_sacral_description
        )
        form.chakra_assessment_solar_plexus_score.data = str(
            note.chakra_assessment_solar_plexus_score
        )
        form.chakra_assessment_solar_plexus_description.data = (
            note.chakra_assessment_solar_plexus_description
        )
        form.chakra_assessment_heart_score.data = str(
            note.chakra_assessment_heart_score
        )
        form.chakra_assessment_heart_description.data = (
            note.chakra_assessment_heart_description
        )
        form.chakra_assessment_throat_score.data = str(
            note.chakra_assessment_throat_score
        )
        form.chakra_assessment_throat_description.data = (
            note.chakra_assessment_throat_description
        )
        form.chakra_assessment_third_eye_score.data = str(
            note.chakra_assessment_third_eye_score
        )
        form.chakra_assessment_third_eye_description.data = (
            note.chakra_assessment_third_eye_description
        )
        form.chakra_assessment_crown_score.data = str(
            note.chakra_assessment_crown_score
        )
        form.chakra_assessment_crown_description.data = (
            note.chakra_assessment_crown_description
        )
        form.visit_notes.data = note.visit_notes
        form.post_visit_recommendations.data = note.post_visit_recommendations

        return render_template(
            "visit_notes/edit_visit_note.html",
            title="Soulstone - Edit Visit Note",
            user=current_user,
            person=person,
            note=note,
            form=form,
            person_header=person_header,
            notes_count=notes_count,
            events_count=events_count,
            balance=balance,
            chakra_graph_labels=chakra_graph_labels,
            chakra_graph_data=chakra_graph_data,
        )

    if form.validate_on_submit() and request.method == "POST":
        note.updated_at = datetime.utcnow()
        note.reason_for_visit = form.reason_for_visit.data
        note.date_of_service = form.date_of_service.data
        note.chakra_assessment_root_score =\
            form.chakra_assessment_root_score.data
        note.chakra_assessment_root_description = (
            form.chakra_assessment_root_description.data
        )
        note.chakra_assessment_sacral_score =\
            form.chakra_assessment_sacral_score.data
        note.chakra_assessment_sacral_description = (
            form.chakra_assessment_sacral_description.data
        )
        note.chakra_assessment_solar_plexus_score = (
            form.chakra_assessment_solar_plexus_score.data
        )
        note.chakra_assessment_solar_plexus_description = (
            form.chakra_assessment_solar_plexus_description.data
        )
        note.chakra_assessment_heart_score =\
            form.chakra_assessment_heart_score.data
        note.chakra_assessment_heart_description = (
            form.chakra_assessment_heart_description.data
        )
        note.chakra_assessment_throat_score =\
            form.chakra_assessment_throat_score.data
        note.chakra_assessment_throat_description = (
            form.chakra_assessment_throat_description.data
        )
        note.chakra_assessment_third_eye_score = (
            form.chakra_assessment_third_eye_score.data
        )
        note.chakra_assessment_third_eye_description = (
            form.chakra_assessment_third_eye_description.data
        )
        note.chakra_assessment_crown_score =\
            form.chakra_assessment_crown_score.data
        note.chakra_assessment_crown_description = (
            form.chakra_assessment_crown_description.data
        )
        note.visit_notes = form.visit_notes.data
        note.post_visit_recommendations = form.post_visit_recommendations.data

        # Update visit note to database
        try:
            db.session.commit()
            flash("Visit Note updated successfully.", category="success")
        except note.GeneralSaveError:
            flash("Something went wrong. Try again.", category="danger")

        return redirect(url_for("visit_notes.notes"))


# Visit Note - Change Status
@visit_notes.route("/change_status/<int:visit_note_id>",
                   methods=["GET", "POST"])
@login_required
def changeStatus(visit_note_id):
    note = Notes.query.filter_by(id=visit_note_id).first_or_404()

    form = ChangeVisitNoteStatusForm()

    if request.method == "GET":
        # If visit note is open,
        # change status default status option to completed
        if note.status == "Open":
            form.status.default = "Completed"
            form.process()

    if form.validate_on_submit() and request.method == "POST":
        note.status = form.status.data
        note.updated_at = datetime.utcnow()
        note.updated_by = current_user.id

        # Update visit note to database
        try:
            db.session.commit()
            flash("Visit Note status updated successfully.",
                  category="success")
        except note.GeneralSaveError:
            flash("Something went wrong. Try again.", category="danger")

        if note.status == "Completed":
            return redirect(url_for("visit_notes.pdfVisitNote", id=note.id))
        return redirect(url_for("visit_notes.editVisitNote", id=note.id))

    return render_template(
        "visit_notes/change_status.html",
        title="Soulstone - Change Status",
        form=form,
        user=current_user,
        note=note,
    )


# Visit Note - Delete
@visit_notes.route("/change_delete/<int:visit_note_id>",
                   methods=["GET", "POST"])
@login_required
def changeStatusDelete(visit_note_id):
    note = Notes.query.filter_by(id=visit_note_id).first_or_404()

    form = DeleteVisitNoteForm()

    if form.validate_on_submit() and request.method == "POST":
        note.status = "Deleted"
        note.updated_at = datetime.utcnow()
        note.updated_by = current_user.id

        # Update visit note to database
        try:
            db.session.commit()
            flash(
                "Visit Note status updated to 'Deleted' successfully.",
                category="success",
            )
        except note.GeneralSaveError:
            flash("Something went wrong. Try again.", category="danger")

        return redirect(url_for("visit_notes.notes"))

    return render_template(
        "visit_notes/delete_visit_note.html",
        title="Soulstone - Delete Visit Note",
        form=form,
        user=current_user,
        note=note,
    )


# Visit Note - PDF Visit Note
@visit_notes.route("/pdf_note/<int:id>")
@login_required
def pdfVisitNote(id):
    note = Notes.query.get_or_404(id)
    practice = Practice.query.filter_by(id=note.practice_id).first()
    person = People.query.filter_by(id=note.person_id).first()

    rendered = render_template(
        "visit_notes/pdf_visit_note.html",
        note=note,
        practice=practice,
        person=person,
        user=current_user,
    )
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=visit_note.pdf"
    return response

# soulstone/website/visit_notes/views.py


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import pdfkit
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import make_response
from flask_login import login_required, current_user
from src.visit_notes.forms import AddVisitNoteForm, EditVisitNoteForm
from src import db
from src.models import People, Practice, Notes, LedgerCharges, LedgerPayments


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
visit_notes = Blueprint('visit_notes', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Notes
# ------------------------------------------------------------------------------
@visit_notes.route('/notes')
@login_required
def notes():
    ''' Routes the user to the Notes page '''
    visit_notes = db.session.query(Notes.id,
                                   Notes.date_of_service,
                                   Notes.status,
                                   Notes.practice_id,
                                   People.first_name,
                                   People.middle_name,
                                   People.last_name,
                                   People.suffix_name)\
        .filter_by(practice_id=current_user.practice_id)\
        .join(People, Notes.person_id == People.id).all()

    people = People.query.filter_by(practice_id=current_user.practice_id).all()

    return render_template("notes.html", title="Soulstone - Notes",
                           user=current_user,
                           visit_notes=visit_notes,
                           people=people)


@visit_notes.route('/notes/<int:id>/add_visit_note', methods=['GET', 'POST'])
@login_required
def addVisitNote(id):
    # TODO: figure out how to select the person before starting the form
    # TODO: should the form be broken up and save each step?

    form = AddVisitNoteForm()

    pers_id = People.query.get_or_404(id).id

    total_charges = db.session.query(db.func.sum(LedgerCharges.units * LedgerCharges.unit_amount + (
        LedgerCharges.unit_amount * LedgerCharges.tax_rate))).filter_by(practice_id=current_user.practice_id, person_id=id).scalar()
    total_payments = db.session.query(db.func.sum(LedgerPayments.amount)).filter_by(
        practice_id=current_user.practice_id, person_id=id).scalar()

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0
    balance = total_charges - total_payments

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = People.query.get_or_404(id).practice_id

    if request.method == 'GET':
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            return render_template("add_visit_note.html",
                                   title="Soulstone - Add Visit Note",
                                   user=current_user,
                                   person=person,
                                   form=form,
                                   balance=balance)
        else:
            return render_template("401.html",
                                   user=current_user)

    if form.validate_on_submit() and request.method == 'POST':
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
        chakra_assessment_root_description = form.chakra_assessment_root_description.data
        chakra_assessment_sacral_score = form.chakra_assessment_sacral_score.data
        chakra_assessment_sacral_description = form.chakra_assessment_sacral_description.data
        chakra_assessment_solar_plexus_score = form.chakra_assessment_solar_plexus_score.data
        chakra_assessment_solar_plexus_description = form.chakra_assessment_solar_plexus_description.data
        chakra_assessment_heart_score = form.chakra_assessment_heart_score.data
        chakra_assessment_heart_description = form.chakra_assessment_heart_description.data
        chakra_assessment_throat_score = form.chakra_assessment_throat_score.data
        chakra_assessment_throat_description = form.chakra_assessment_throat_description.data
        chakra_assessment_third_eye_score = form.chakra_assessment_third_eye_score.data
        chakra_assessment_third_eye_description = form.chakra_assessment_third_eye_description.data
        chakra_assessment_crown_score = form.chakra_assessment_crown_score.data
        chakra_assessment_crown_description = form.chakra_assessment_crown_description.data
        visit_notes = form.visit_notes.data
        post_visit_recommendations = form.post_visit_recommendations.data

        # Add new visit note to database
        new_visit_note = Notes(practice_id=practice_id,
                               person_id=person_id,
                               created_at=created_at,
                               created_by=created_by,
                               updated_at=updated_at,
                               updated_by=updated_by,
                               date_of_service=date_of_service,
                               reason_for_visit=reason_for_visit,
                               chakra_assessment_root_score=chakra_assessment_root_score,
                               chakra_assessment_root_description=chakra_assessment_root_description,
                               chakra_assessment_sacral_score=chakra_assessment_sacral_score,
                               chakra_assessment_sacral_description=chakra_assessment_sacral_description,
                               chakra_assessment_solar_plexus_score=chakra_assessment_solar_plexus_score,
                               chakra_assessment_solar_plexus_description=chakra_assessment_solar_plexus_description,
                               chakra_assessment_heart_score=chakra_assessment_heart_score,
                               chakra_assessment_heart_description=chakra_assessment_heart_description,
                               chakra_assessment_throat_score=chakra_assessment_throat_score,
                               chakra_assessment_throat_description=chakra_assessment_throat_description,
                               chakra_assessment_third_eye_score=chakra_assessment_third_eye_score,
                               chakra_assessment_third_eye_description=chakra_assessment_third_eye_description,
                               chakra_assessment_crown_score=chakra_assessment_crown_score,
                               chakra_assessment_crown_description=chakra_assessment_crown_description,
                               visit_notes=visit_notes,
                               post_visit_recommendations=post_visit_recommendations)
        db.session.add(new_visit_note)
        db.session.commit()
        flash('Visit Note created successfully.', category='success')

        # Redirect to Visit Notes page
        return redirect(url_for('visit_notes.notes'))


@visit_notes.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def editVisitNote(id):
    form = EditVisitNoteForm()

    note = Notes.query.get_or_404(id)
    pers_id = note.person_id
    person = People.query.get_or_404(pers_id)

    total_charges = db.session.query(db.func.sum(LedgerCharges.units * LedgerCharges.unit_amount + (
        LedgerCharges.unit_amount * LedgerCharges.tax_rate))).filter_by(practice_id=current_user.practice_id, person_id=id).scalar()
    total_payments = db.session.query(db.func.sum(LedgerPayments.amount)).filter_by(
        practice_id=current_user.practice_id, person_id=id).scalar()

    if total_charges is None:
        total_charges = 0
    if total_payments is None:
        total_payments = 0
    balance = total_charges - total_payments

    if request.method == 'GET':
        form.reason_for_visit.data = note.reason_for_visit
        form.date_of_service.data = note.date_of_service
        form.chakra_assessment_root_score.data = note.chakra_assessment_root_score
        form.chakra_assessment_root_description.data = note.chakra_assessment_root_description
        form.chakra_assessment_sacral_score.data = note.chakra_assessment_sacral_score
        form.chakra_assessment_sacral_description.data = note.chakra_assessment_sacral_description
        form.chakra_assessment_solar_plexus_score.data = note.chakra_assessment_solar_plexus_score
        form.chakra_assessment_solar_plexus_description.data = note.chakra_assessment_solar_plexus_description
        form.chakra_assessment_heart_score.data = note.chakra_assessment_heart_score
        form.chakra_assessment_heart_description.data = note.chakra_assessment_heart_description
        form.chakra_assessment_throat_score.data = note.chakra_assessment_throat_score
        form.chakra_assessment_throat_description.data = note.chakra_assessment_throat_description
        form.chakra_assessment_third_eye_score.data = note.chakra_assessment_third_eye_score
        form.chakra_assessment_third_eye_description.data = note.chakra_assessment_third_eye_description
        form.chakra_assessment_crown_score.data = note.chakra_assessment_crown_score
        form.chakra_assessment_crown_description.data = note.chakra_assessment_crown_description
        form.visit_notes.data = note.visit_notes
        form.post_visit_recommendations.data = note.post_visit_recommendations

        return render_template("edit_visit_note.html",
                               title="Soulstone - Edit Visit Note",
                               user=current_user,
                               person=person,
                               note=note,
                               form=form,
                               balance=balance)

    if form.validate_on_submit() and request.method == 'POST':
        note.updated_at = datetime.utcnow()
        note.reason_for_visit = form.reason_for_visit.data
        note.date_of_service = form.date_of_service.data
        note.chakra_assessment_root_score = form.chakra_assessment_root_score.data
        note.chakra_assessment_root_description = form.chakra_assessment_root_description.data
        note.chakra_assessment_sacral_score = form.chakra_assessment_sacral_score.data
        note.chakra_assessment_sacral_description = form.chakra_assessment_sacral_description.data
        note.chakra_assessment_solar_plexus_score = form.chakra_assessment_solar_plexus_score.data
        note.chakra_assessment_solar_plexus_description = form.chakra_assessment_solar_plexus_description.data
        note.chakra_assessment_heart_score = form.chakra_assessment_heart_score.data
        note.chakra_assessment_heart_description = form.chakra_assessment_heart_description.data
        note.chakra_assessment_throat_score = form.chakra_assessment_throat_score.data
        note.chakra_assessment_throat_description = form.chakra_assessment_throat_description.data
        note.chakra_assessment_third_eye_score = form.chakra_assessment_third_eye_score.data
        note.chakra_assessment_third_eye_description = form.chakra_assessment_third_eye_description.data
        note.chakra_assessment_crown_score = form.chakra_assessment_crown_score.data
        note.chakra_assessment_crown_description = form.chakra_assessment_crown_description.data
        note.visit_notes = form.visit_notes.data
        note.post_visit_recommendations = form.post_visit_recommendations.data

        # Update visit note to database
        try:
            db.session.commit()
            flash('Visit Note updated successfully.',
                  category='success')
        except:
            flash('Something went wrong. Try again.',
                  category='danger')

        return redirect(url_for('visit_notes.notes'))


@visit_notes.route('/pdf_note/<int:id>')
@login_required
def pdfVisitNote(id):
    note = Notes.query.get_or_404(id)
    practice = Practice.query.filter_by(id=note.practice_id).first()
    person = People.query.filter_by(id=note.person_id).first()
    rendered = render_template('pdf_visit_note.html',
                               note=note,
                               practice=practice,
                               person=person,
                               user=current_user)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=visit_note.pdf'
    return response

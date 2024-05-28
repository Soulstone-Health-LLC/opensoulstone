"""Support > Views - This file contains the views for the Support Blueprint."""
# Imports
import random
import string
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from support.forms import AddPracticeForm, PracticeUserForm, ReleaseNotesForm
from app import db
from settings.models import Practice
from .models import ReleaseNotes
from users.models import User
from decorators.decorators import support_required


# Blueprint Configuration
supportapp = Blueprint("supportapp", __name__)


# Support - Practices
@supportapp.route("/support")
@login_required
@support_required
def support():
    """Support home page"""

    practices = Practice.query.order_by(Practice.id).all()

    return render_template(
        "support/support.html", practices=practices
    )


# Support - Practices - View Practice
@supportapp.route("/support/<int:practice_id>")
@login_required
@support_required
def view_practice(practice_id):
    """View practice page"""

    practice = Practice.query.get_or_404(practice_id)
    practice_users = User.query.filter_by(practice_id=practice_id).all()

    return render_template(
        "support/support_practice.html",
        practice=practice,
        practice_users=practice_users,
    )


# Support - Practices - Add Practice
@ supportapp.route("/support/add_practice", methods=["GET", "POST"])
@ login_required
@ support_required
def add_practice():
    """Add practice form and page"""

    form = AddPracticeForm()

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        new_practice = Practice()
        form.populate_obj(new_practice)
        new_practice.created_by = current_user.id
        db.session.add(new_practice)
        db.session.commit()
        flash(f"{new_practice.name} created successfully.", category="success")

        # Redirect user to the Support home page
        return redirect(url_for("supportapp.support"))

    return render_template(
        "support/add_practice.html",
        title="Soulstone - Add Practice",
        form=form
    )


# Support - Practices - Edit Practice
@ supportapp.route("/support/edit_practice/<int:practice_id>",
                   methods=["GET", "POST"])
@ login_required
@ support_required
def edit_practice(practice_id):
    """Edit practice form and page"""

    practice = Practice.query.get_or_404(practice_id)
    form = AddPracticeForm(obj=practice)

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        form.populate_obj(practice)
        practice.updated_by = current_user.id
        practice.updated_at = datetime.now(tz=timezone.utc)
        db.session.commit()
        flash(f"{practice.name} updated successfully.", category="success")

        # Redirect user to the Support home page
        return redirect(url_for("supportapp.support"))

    return render_template(
        "support/add_practice.html",
        title="Soulstone - Edit Practice",
        form=form
    )


# Support - Practices - Add Practice User
@ supportapp.route("/support/<int:practice_id>/support_add_user",
                   methods=["GET", "POST"])
@ login_required
@ support_required
def add_practice_user(practice_id):
    """Add practice user form and page"""

    form = PracticeUserForm()
    practice = Practice.query.get(practice_id)

    # Random string
    def randompass(length):
        """Generates a random string for a temporary password"""
        s = string
        letters = s.ascii_lowercase + s.ascii_uppercase + s.digits
        return "".join(random.choice(letters) for i in range(length))

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            practice_id = request.form.get("practice_id")
            role = form.role.data
            firstname = form.first_name.data
            middlename = form.middle_name.data
            lastname = form.last_name.data
            suffix = form.suffix_name.data
            email = form.email.data
            phonenumber = form.phone.data
            phonetype = form.phone_type.data
            password = randompass(10)

            # Add new practice user to database
            new_practice_user = User(
                practice_id=practice_id,
                role=role,
                first_name=firstname,
                middle_name=middlename,
                last_name=lastname,
                suffix_name=suffix,
                email=email,
                password=generate_password_hash(password),
                phone_number=phonenumber,
                phone_type=phonetype,
                status="Active",
            )
            db.session.add(new_practice_user)
            db.session.commit()
            flash(f"{form.email} created successfully.", category="success")

            # Redirect user to Support home page
            return redirect(url_for("supportapp.view_practice",
                                    practice_id=practice_id))

    return render_template(
        "support/support_add_user.html",
        title="Soulstone - Add Practice User",
        user=current_user,
        form=form,
        practice=practice,
    )


# Support App - Release Notes - View list of Release Notes
@ supportapp.route("/support/release_notes")
@ login_required
@ support_required
def view_release_notes():
    """View release notes form and page"""

    release_notes = ReleaseNotes.query.order_by(
        ReleaseNotes.release_note_date.desc()
    ).all()

    return render_template(
        "support/support_release_notes.html",
        user=current_user,
        release_notes=release_notes,
    )


# Support App - Release Notes - Add Release Note
@ supportapp.route("/support/add_release_notes", methods=["GET", "POST"])
@ login_required
@ support_required
def add_release_notes():
    """Add release notes form and page"""

    form = ReleaseNotesForm()

    # If the user hits cancel, redirect to the Release Notes list page
    if form.cancel.data:
        return redirect(url_for("supportapp.view_release_notes"))

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            release_note_date = form.release_note_date.data
            release_note_content = form.release_note_content.data

        # Add new release notes to database
        new_release_notes = ReleaseNotes(
            release_note_date=release_note_date,
            release_note_content=release_note_content,
            created_by=current_user.id,
            created_at=datetime.now(tz=timezone.utc),
        )
        db.session.add(new_release_notes)
        db.session.commit()
        flash("Release note created successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(url_for("supportapp.view_release_notes"))

    return render_template(
        "support/add_release_notes.html",
        title="Soulstone - Add Release Notes",
        form=form,
        user=current_user,
    )


# Support App - Release Notes - View a Release Note
@ supportapp.route("/support/release_notes/<int:release_note_id>")
@ login_required
@ support_required
def view_release_note_details(release_note_id):
    """View release note details form and page"""

    release_notes = ReleaseNotes.query.get_or_404(release_note_id)

    return render_template(
        "support/support_view_release_note.html",
        user=current_user,
        release_notes=release_notes,
    )


# Support App - Release Notes - Edit Release Note
@ supportapp.route(
    "/support/edit_release_notes/<int:release_note_id>",
    methods=["GET", "POST"]
)
@ login_required
@ support_required
def edit_release_notes(release_note_id):
    """Edit release notes form and page"""

    form = ReleaseNotesForm()

    # Pre-populate the form with the existing data
    if request.method == "GET":
        release_notes = ReleaseNotes.query.get_or_404(release_note_id)
        form.release_note_date.data = release_notes.release_note_date
        form.release_note_content.data = release_notes.release_note_content

    # If the user hits cancel, redirect to the Release Notes list page
    if form.cancel.data:
        return redirect(
            url_for(
                "supportapp.view_release_note_details",
                release_note_id=release_note_id
            )
        )

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            release_note_date = form.release_note_date.data
            release_note_content = form.release_note_content.data

        # Update release notes in database
        release_notes = ReleaseNotes.query.get_or_404(release_note_id)
        release_notes.release_note_date = release_note_date
        release_notes.release_note_content = release_note_content
        release_notes.updated_by = current_user.id
        release_notes.updated_at = datetime.now(tz=timezone.utc)
        db.session.commit()
        flash("Release note updated successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(
            url_for(
                "supportapp.view_release_note_details",
                release_note_id=release_note_id
            )
        )

    return render_template(
        "support/add_release_notes.html",
        title="Soulstone - Edit Release Notes",
        form=form,
        user=current_user,
    )


# Support App - Release Notes - Delete Release Note
@ supportapp.route("/support/delete_release_notes/<int:release_note_id>")
@ login_required
@ support_required
def delete_release_notes(release_note_id):
    """Delete release notes from database"""

    release_notes = ReleaseNotes.query.get_or_404(release_note_id)
    db.session.delete(release_notes)
    db.session.commit()
    flash("Release note deleted successfully.", category="success")

    # Redirect user to the Release Notes list page
    return redirect(url_for("supportapp.view_release_notes"))

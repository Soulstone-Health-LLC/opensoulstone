"""Support > Views - This file contains the views for the Support Blueprint."""
# Imports
from datetime import datetime, timezone
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from universal.controls import send_email, randompass
from users.models import User
from decorators.decorators import support_required
from settings.models import Practice
from app import db
from .models import ReleaseNotes
from .forms import AddPracticeForm, PracticeUserForm, ReleaseNotesForm


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
@supportapp.route("/support/add_practice", methods=["GET", "POST"])
@login_required
@support_required
def add_practice():
    """Add practice form and page"""

    form = AddPracticeForm()

    # Gets the data from the form and saves to the database
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
@supportapp.route("/support/edit_practice/<int:practice_id>",
                  methods=["GET", "POST"])
@login_required
@support_required
def edit_practice(practice_id):
    """Edit practice form and page"""

    practice = Practice.query.get_or_404(practice_id)
    form = AddPracticeForm(obj=practice)

    # Gets the data from the form and saves to the database
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
@supportapp.route("/support/<int:practice_id>/support_add_user",
                  methods=["GET", "POST"])
@login_required
@support_required
def add_practice_user(practice_id):
    """Add practice user form and page"""

    form = PracticeUserForm()
    practice = Practice.query.get(practice_id)
    random_password = randompass(10)

    # Gets the data from the form and saves to the database
    if form.validate_on_submit():
        new_practice_user = User()
        form.populate_obj(new_practice_user)
        new_practice_user.practice_id = practice_id
        new_practice_user.password = generate_password_hash(random_password)
        new_practice_user.created_by = current_user.id
        db.session.add(new_practice_user)
        db.session.commit()

        # Send email to user
        send_email('Soulstone - Account Created',
                   new_practice_user.email,
                   f"Your Soulstone account has been created for {
                       practice.name}."
                   f"\n\nEmail: {new_practice_user.email}"
                   f"\nTemporary Password: {random_password}"
                   f"\n\nPlease login at: https://soulstone.app/login"
                   f"\nand update your password at your earliest convenience."
                   f"\n\nThank you!"
                   f"\nSoulstone Support")

        flash(f"{form.email} created successfully and email sent to user.",
              category="success")

        # Redirect user to Support home page
        return redirect(url_for("supportapp.view_practice",
                                practice_id=practice_id))

    return render_template(
        "support/support_add_user.html",
        title="Soulstone - Add Practice User",
        form=form,
        practice=practice
    )


# Support App - Release Notes - View list of Release Notes
@supportapp.route("/support/release_notes")
@login_required
@support_required
def view_release_notes():
    """View release notes form and page"""

    release_notes = ReleaseNotes.query.order_by(
        ReleaseNotes.release_note_date.desc()
    ).all()

    return render_template(
        "support/support_release_notes.html",
        release_notes=release_notes
    )


# Support App - Release Notes - Add Release Note
@supportapp.route("/support/add_release_notes", methods=["GET", "POST"])
@login_required
@support_required
def add_release_notes():
    """Add release notes form and page"""

    form = ReleaseNotesForm()

    # If the user hits cancel, redirect to the Release Notes list page
    if form.cancel.data:
        return redirect(url_for("supportapp.view_release_notes"))

    # Gets the data from the form and saves to the database
    if form.validate_on_submit():
        new_release_notes = ReleaseNotes()
        form.populate_obj(new_release_notes)
        new_release_notes.created_by = current_user.id
        db.session.add(new_release_notes)
        db.session.commit()
        flash("Release note created successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(url_for("supportapp.view_release_notes"))

    return render_template("support/add_release_notes.html",
                           title="Soulstone - Add Release Notes", form=form
                           )


# Support App - Release Notes - View a Release Note
@supportapp.route("/support/release_notes/<int:release_note_id>")
@login_required
@support_required
def view_release_note_details(release_note_id):
    """View release note details form and page"""

    release_notes = ReleaseNotes.query.get_or_404(release_note_id)

    return render_template(
        "support/support_view_release_note.html",
        user=current_user,
        release_notes=release_notes,
    )


# Support App - Release Notes - Edit Release Note
@supportapp.route("/support/edit_release_notes/<int:release_note_id>",
                  methods=["GET", "POST"])
@login_required
@support_required
def edit_release_notes(release_note_id):
    """Edit release notes form and page"""

    release_note = ReleaseNotes.query.get_or_404(release_note_id)
    form = ReleaseNotesForm(obj=release_note)

    # If the user hits cancel, redirect to the Release Notes list page
    if form.cancel.data:
        return redirect(
            url_for("supportapp.view_release_note_details",
                    release_note_id=release_note_id)
        )

    if form.validate_on_submit():
        form.populate_obj(release_note)
        release_note.updated_by = current_user.id
        release_note.updated_at = datetime.now(tz=timezone.utc)
        db.session.commit()
        flash("Release note updated successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(
            url_for("supportapp.view_release_note_details",
                    release_note_id=release_note_id)
        )

    return render_template(
        "support/add_release_notes.html",
        title="Soulstone - Edit Release Notes", form=form)


# Support App - Release Notes - Delete Release Note
@supportapp.route("/support/delete_release_notes/<int:release_note_id>")
@login_required
@support_required
def delete_release_notes(release_note_id):
    """Delete release notes from database"""

    release_note = ReleaseNotes.query.get_or_404(release_note_id)
    db.session.delete(release_note)
    db.session.commit()
    flash("Release note deleted successfully.", category="success")

    # Redirect user to the Release Notes list page
    return redirect(url_for("supportapp.view_release_notes"))

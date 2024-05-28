"""
Support > Views - This file contains the views for the Support Blueprint.
"""

# Imports
import random
import string
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from support.forms import (
    AddPracticeForm, PracticeUserForm, ReleaseNotesForm
)
from app import db
from settings.models import Practice
from support.models import ReleaseNotes
from users.models import User
from decorators.decorators import support_required


# Blueprint Configuration
supportapp = Blueprint("supportapp", __name__)


# Support - Practices
@supportapp.route("/support")
@login_required
@support_required
def support():

    practices = Practice.query.order_by(Practice.id).all()

    return render_template(
        "support/support.html", user=current_user, practices=practices
    )


# Support - Practices - View Practice
@supportapp.route("/support/<int:id>")
@login_required
@support_required
def viewpractice(id):
    practice = Practice.query.get_or_404(id)
    practice_user = User.query.order_by(User.last_name).all()
    return render_template(
        "support/support_practice.html",
        user=current_user,
        practice=practice,
        practice_user=practice_user,
    )


# Support - Practices - Add Practice
@supportapp.route("/support/add_practice", methods=["GET", "POST"])
@login_required
@support_required
def addpractice():
    """Add practice form and page"""
    form = AddPracticeForm()

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            name = form.name.data
            biography = form.biography.data
            address_1 = form.address_1.data
            address_2 = form.address_2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            email = form.email.data
            website = form.website.data
            phone_number = form.phone.data
            phone_type = form.phone_type.data

        # Add new practice to database
        new_practice = Practice(
            name=name,
            biography=biography,
            address_1=address_1,
            address_2=address_2,
            city=city,
            state=state,
            zipcode=zipcode,
            email=email,
            website=website,
            phone_number=phone_number,
            phone_type=phone_type,
        )
        db.session.add(new_practice)
        db.session.commit()
        flash(f"{name} created successfully.", category="success")

        # Redirect user to the Support home page
        return redirect(url_for("views.support"))

    return render_template(
        "support/add_practice.html",
        title="Soulstone - Add Practice",
        form=form,
        user=current_user,
    )


# Support - Practices - Add Practice User
@supportapp.route("/support/<int:id>/support_add_user",
                  methods=["GET", "POST"])
@login_required
@support_required
def addPracticeUser(id):
    """Add practice user form and page"""
    form = PracticeUserForm()
    practice = Practice.query.get(id)

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
                password=generate_password_hash(password, method="sha384"),
                phone_number=phonenumber,
                phone_type=phonetype,
                status="Active",
            )
            db.session.add(new_practice_user)
            db.session.commit()
            flash(f"{form.email} created successfully.", category="success")

            # Redirect user to Support home page
            return redirect(url_for("supportapp.support"))

    return render_template(
        "support/support_add_user.html",
        title="Soulstone - Add Practice User",
        user=current_user,
        form=form,
        practice=practice,
    )


# Support App - Release Notes - View list of Release Notes
@supportapp.route("/support/release_notes")
@login_required
@support_required
def viewReleaseNotes():
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
@supportapp.route("/support/add_release_notes", methods=["GET", "POST"])
@login_required
@support_required
def addReleaseNotes():
    """Add release notes form and page"""

    form = ReleaseNotesForm()

    # If the user hits cancel, redirect to the Release Notes list page
    if form.cancel.data:
        return redirect(url_for("supportapp.viewReleaseNotes"))

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
            created_at=datetime.now(),
        )
        db.session.add(new_release_notes)
        db.session.commit()
        flash("Release note created successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(url_for("supportapp.viewReleaseNotes"))

    return render_template(
        "support/add_release_notes.html",
        title="Soulstone - Add Release Notes",
        form=form,
        user=current_user,
    )


# Support App - Release Notes - View a Release Note
@supportapp.route("/support/release_notes/<int:release_note_id>")
@login_required
@support_required
def viewReleaseNoteDetails(release_note_id):
    """View release note details form and page"""

    release_notes = ReleaseNotes.query.get_or_404(release_note_id)

    return render_template(
        "support/support_view_release_note.html",
        user=current_user,
        release_notes=release_notes,
    )


# Support App - Release Notes - Edit Release Note
@supportapp.route(
    "/support/edit_release_notes/<int:release_note_id>",
    methods=["GET", "POST"]
)
@login_required
@support_required
def editReleaseNotes(release_note_id):
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
                "supportapp.viewReleaseNoteDetails",
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
        release_notes.updated_at = datetime.now()
        db.session.commit()
        flash("Release note updated successfully.", category="success")

        # Redirect user to the Release Notes list page
        return redirect(
            url_for(
                "supportapp.viewReleaseNoteDetails",
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
@supportapp.route("/support/delete_release_notes/<int:release_note_id>")
@login_required
@support_required
def deleteReleaseNotes(release_note_id):
    """Delete release notes from database"""

    release_notes = ReleaseNotes.query.get_or_404(release_note_id)
    db.session.delete(release_notes)
    db.session.commit()
    flash("Release note deleted successfully.", category="success")

    # Redirect user to the Release Notes list page
    return redirect(url_for("supportapp.viewReleaseNotes"))

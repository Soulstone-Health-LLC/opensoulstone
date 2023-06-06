"""
Core > Views - This file contains the views for the Core Blueprint.
"""

# Imports
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from src.models import ReleaseNotes
from src import db


# Blueprint Configuration
core = Blueprint("core", __name__)


# Homepage
@core.route("/")
@login_required
def home():
    """Home page"""

    return redirect(url_for("persons.people"))


# Release Notes
@core.route("/release_notes")
@login_required
def release_notes_page():
    """Release Notes page"""

    # Query for the 10 most recent release notes
    release_notes = (
        db.session.query(ReleaseNotes)
        .order_by(ReleaseNotes.release_note_date.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "core/release_notes.html",
        release_notes=release_notes,
        user=current_user,
    )

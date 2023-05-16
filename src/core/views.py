"""
Core > Views - This file contains the views for the Core Blueprint.
"""

# Imports
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


# Blueprint Configuration
core = Blueprint("core", __name__)


# Homepage
@core.route("/")
@login_required
def home():
    """Home page"""

    return redirect(url_for("persons.people"))

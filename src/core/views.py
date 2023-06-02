"""
Core > Views - This file contains the views for the Core Blueprint.
"""

# Imports
from flask import Blueprint, redirect, url_for
from flask_login import login_required


# Blueprint Configuration
core = Blueprint("core", __name__)


# Homepage
@core.route("/")
@login_required
def home():
    """Home page"""

    return redirect(url_for("persons.people"))

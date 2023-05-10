"""
Core > Views - This file contains the views for the Core Blueprint.
"""

# Imports
from flask import Blueprint, render_template
from flask_login import login_required, current_user


# Blueprint Configuration
core = Blueprint("core", __name__)


# Homepage
@core.route("/")
@login_required
def home():
    """Home page"""
    return render_template("core/home.html", title="Soulstone",
                           user=current_user)

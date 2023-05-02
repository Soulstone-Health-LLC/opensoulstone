# soulstone/website/core/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template
from flask_login import login_required, current_user


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
core = Blueprint('core', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Dashboard
# ------------------------------------------------------------------------------
# Homepage
@core.route('/')
@login_required
def home():
    '''Home page'''
    return render_template("core/home.html", title="Soulstone", user=current_user)

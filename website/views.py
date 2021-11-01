'''
    File name: views.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

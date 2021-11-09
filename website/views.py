'''
    File name: views.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
# from .models import Pet
from . import db


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
views = Blueprint('views', __name__)


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/support')
@login_required
def support():
    return render_template("support.html", user=current_user)


@views.route('/support/add_practice')
@login_required
def addpractice():
    return render_template("add_practice.html", user=current_user)
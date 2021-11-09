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
from .models import Practice
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


@views.route('/support/add_practice', methods=['GET', 'POST'])
@login_required
def addpractice():
    '''Add practice form and page'''
    # Gets the data from the form and saves as variables
    if request.method == 'POST':
        practicename = request.form.get('practicename')
        biography = request.form.get('biography')
        email = request.form.get('email')
        website = request.form.get('website')
        phonenumber = request.form.get('phonenumber')
        phonetype = request.form.get('phonetype')
        
        # Add new user to database
        new_practice = Practice(name=practicename, biography=biography,
                                email=email, website=website,
                                phone_number=phonenumber,
                                phone_type=phonetype)
        db.session.add(new_practice)
        db.session.commit()
        flash(' Account created!', category='success')
        return redirect(url_for('views.support'))
    return render_template("add_practice.html", user=current_user)
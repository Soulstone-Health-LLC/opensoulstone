'''
    File name: views.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from flask_login import login_required, current_user
from .models import People, Practice
from . import db
from datetime import datetime


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
views = Blueprint('views', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice
# ------------------------------------------------------------------------------
# Homepage
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


# People
@views.route('/people')
@login_required
def people():
    if request.method == 'GET':
        people = People.query.order_by(People.last_name).all()
    return render_template("people.html", user=current_user, people=people)
    


# ------------------------------------------------------------------------------
# Routes - Support
# ------------------------------------------------------------------------------
# Support - Practices
@views.route('/support')
@login_required
def support():
    if request.method == "GET":
        practices = Practice.query.order_by(Practice.created_at).all()
    return render_template("support.html", user=current_user, practices=practices)


# Support - Practices - View Practice
@views.route('/support/<int:id>')
def viewpractice(id):
    practice = Practice.query.get_or_404(id)
    return render_template("support_practice.html", user=current_user, practice=practice)


# Support - Practices - Add Practice
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
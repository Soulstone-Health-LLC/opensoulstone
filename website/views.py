'''
    File name: views.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import random
import string
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .models import People, Practice, User


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
views = Blueprint('views', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice
# ------------------------------------------------------------------------------
# 404 Page
@views.errorhandler(404)
def page_not_found():
    ''' Displays 404 page if there is an error '''
    return render_template("404.html", title='Soulstone'), 404


# ------------------------------------------------------------------------------
# Routes - Practice
# ------------------------------------------------------------------------------
# Homepage
@views.route('/')
@login_required
def home():
    return render_template("home.html", title="Soulstone", user=current_user)


# People
@views.route('/people')
@login_required
def people():
    if request.method == 'GET':
        people = People.query.order_by(People.last_name).all()
    return render_template("people.html", title="Soulstone - People",
                           user=current_user, people=people)


# Notes
@views.route('/notes')
@login_required
def notes():
    ''' Routes the user to the Notes page '''
    return render_template("notes.html", title="Soulstone - Notes",
                           user=current_user)


# Billing
@views.route('/billing')
@login_required
def billing():
    ''' Routes the user to the Billing page '''
    return render_template("billing.html", title="Soulstone - Billing",
                           user=current_user)


# ------------------------------------------------------------------------------
# Routes - Support
# ------------------------------------------------------------------------------
# Support - Practices
@views.route('/support')
@login_required
def support():
    if request.method == "GET":
        practices = Practice.query.order_by(Practice.id).all()
    return render_template("support.html", user=current_user,
                           practices=practices)


# Support - Practices - View Practice
@views.route('/support/<int:id>')
def viewpractice(id):
    practice = Practice.query.get_or_404(id)
    practice_user = User.query.order_by(User.last_name).all()
    return render_template("support_practice.html", user=current_user,
                           practice=practice, practice_user=practice_user)


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

        # Add new practice to database
        new_practice = Practice(name=practicename, biography=biography,
                                email=email, website=website,
                                phone_number=phonenumber,
                                phone_type=phonetype)
        db.session.add(new_practice)
        db.session.commit()
        flash(' Account created!', category='success')
        return redirect(url_for('views.support'))
    return render_template("add_practice.html", user=current_user)


# Support - Practices - Add Practice User
@views.route('/support/<int:id>/support_add_user', methods=['GET', 'POST'])
@login_required
def addPracticeUser(id):
    '''Add practice user form and page'''
    practice = Practice.query.get(id)

    # Random string
    def randompass(length):
        ''' Generates a random string for a temporary password '''
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    # Gets the data from the form and saves as variables
    if request.method == 'POST':
        practice_id = request.form.get('practice_id')
        role = request.form.get('role')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        suffix = request.form.get('suffix')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        phonetype = request.form.get('phonetype')
        password = randompass(10)

        # Add new practice user to database
        new_practice_user = User(practice_id=practice_id,
                                 role=role,
                                 first_name=firstname,
                                 middle_name=middlename,
                                 last_name=lastname,
                                 suffix_name=suffix,
                                 email=email,
                                 password=generate_password_hash(password, method='sha384'),
                                 phone_number=phonenumber,
                                 phone_type=phonetype,
                                 status='Active')
        db.session.add(new_practice_user)
        db.session.commit()
        flash(' Account created!', category='success')
        return redirect(url_for('views.support'))
    return render_template("support_add_user.html", user=current_user, practice=practice)

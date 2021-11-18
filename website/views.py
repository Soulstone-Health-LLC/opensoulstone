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
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .forms import AddPersonForm, AddPracticeForm, AddPracticeUserForm
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
@views.errorhandler(401)
def page_401(e):
    ''' Displays 401 page if there is an error '''
    return render_template("401.html", title='Soulstone'), 401


# 404 Page
@views.errorhandler(404)
def page_404(e):
    ''' Displays 404 page if there is an error '''
    return render_template("404.html", title='Soulstone')


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
    practice = current_user.practice_id
    if request.method == 'GET':
        people = People.query.order_by(People.last_name).all()

    return render_template("people.html",
                           title="Soulstone - People",
                           user=current_user,
                           people=people)


# People - Add New Person
@views.route('/people/add_person', methods=['GET', 'POST'])
@login_required
def addPerson():
    form = AddPersonForm()

    print(f'User\'s id: {current_user.get_id()}')
    print(f'User\'s practice id: {current_user.practice_id}')

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            first_name = form.first_name.data
            middle_name = form.middle_name.data
            last_name = form.last_name.data
            suffix = form.suffix_name.data
            address_1 = form.address_1.data
            address_2 = form.address_2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            phone_number = form.phone.data
            phone_type = form.phone_type.data
            email = form.email.data
            status = form.status.data

            # Add new practice to database
            new_person = People(practice_id=practice_id,
                                created_at=created_at,
                                created_by=created_by,
                                updated_at=updated_at,
                                updated_by=updated_by,
                                first_name=first_name,
                                middle_name=middle_name,
                                last_name=last_name,
                                suffix_name=suffix,
                                address_1=address_1,
                                address_2=address_2,
                                city=city,
                                state=state,
                                zipcode=zipcode,
                                phone_number=phone_number,
                                phone_type=phone_type,
                                email=email,
                                status=status)
            db.session.add(new_person)
            db.session.commit()
            flash(f'{first_name} {last_name} created successfully.',
                  category='success')

    return render_template("add_people.html",
                           title="Soulstone - Add Person",
                           user=current_user,
                           form=form)


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
    return render_template("support.html",
                           user=current_user,
                           practices=practices)


# Support - Practices - View Practice
@views.route('/support/<int:id>')
def viewpractice(id):
    practice = Practice.query.get_or_404(id)
    practice_user = User.query.order_by(User.last_name).all()
    return render_template("support_practice.html",
                           user=current_user,
                           practice=practice,
                           practice_user=practice_user)


# Support - Practices - Add Practice
@views.route('/support/add_practice', methods=['GET', 'POST'])
@login_required
def addpractice():
    '''Add practice form and page'''
    form = AddPracticeForm()

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == 'POST':
            name = form.name.data
            biography = form.biography.data
            email = form.email.data
            website = form.website.data
            phone_number = form.phone.data
            phone_type = form.phone_type.data

        # Add new practice to database
        new_practice = Practice(name=name,
                                biography=biography,
                                email=email,
                                website=website,
                                phone_number=phone_number,
                                phone_type=phone_type)
        db.session.add(new_practice)
        db.session.commit()
        flash(f'{name} created successfully.', category='success')

        # Redirect user to the Support home page
        return redirect(url_for('views.support'))

    return render_template("add_practice.html",
                           title="Soulstone - Add Practice",
                           form=form,
                           user=current_user)


# Support - Practices - Add Practice User
@views.route('/support/<int:id>/support_add_user', methods=['GET', 'POST'])
@login_required
def addPracticeUser(id):
    '''Add practice user form and page'''
    form = AddPracticeUserForm()
    practice = Practice.query.get(id)

    # Random string
    def randompass(length):
        ''' Generates a random string for a temporary password '''
        s = string
        letters = s.ascii_lowercase + s.ascii_uppercase + s.digits
        return ''.join(random.choice(letters) for i in range(length))

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == 'POST':
            practice_id = request.form.get('practice_id')
            role = form.role.data
            firstname = form.first_name.data
            middlename = form.middle_name.data
            lastname = form.last_name.data
            suffix = form.suffix_name.data
            email = form.email.data
            phonenumber = form.phone.data
            phonetype = form.phone_type.data
            password = randompass(10)

            # Add new practice user to database
            new_practice_user = User(practice_id=practice_id,
                                     role=role,
                                     first_name=firstname,
                                     middle_name=middlename,
                                     last_name=lastname,
                                     suffix_name=suffix,
                                     email=email,
                                     password=generate_password_hash(
                                         password, method='sha384'),
                                     phone_number=phonenumber,
                                     phone_type=phonetype,
                                     status='Active')
            db.session.add(new_practice_user)
            db.session.commit()
            flash(f'{form.email} created successfully.', category='success')

            # Redirect user to Support home page
            return redirect(url_for('views.support'))

    return render_template("support_add_user.html",
                           title="Soulstone - Add Practice User",
                           user=current_user,
                           form=form,
                           practice=practice)

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
from .forms import AddChargeForm, AddPersonForm, AddVisitNoteForm, EditChargeForm, EditPersonForm, AddPracticeForm, AddPracticeUserForm, EditPracticeForm
from . import db
from .models import Charges, People, Practice, User


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
views = Blueprint('views', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Error Pages
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
# Routes - Practice - Dashboard
# ------------------------------------------------------------------------------
# Homepage
@views.route('/')
@login_required
def home():
    return render_template("home.html", title="Soulstone", user=current_user)


# ------------------------------------------------------------------------------
# Routes - Practice - People
# ------------------------------------------------------------------------------
# People
@views.route('/people')
@login_required
def people():
    if request.method == 'GET':
        people = People.query.filter_by(practice_id=current_user.practice_id).order_by(People.last_name).all()

    return render_template("people.html",
                           title="Soulstone - People",
                           user=current_user,
                           people=people)


# People - Add New Person
@views.route('/people/add_person', methods=['GET', 'POST'])
@login_required
def addPerson():
    form = AddPersonForm()

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
            date_of_birth = form.date_of_birth.data
            gender_identity = form.gender_identity.data
            address_1 = form.address_1.data
            address_2 = form.address_2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            phone_number = form.phone.data
            phone_type = form.phone_type.data
            email = form.email.data

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
                                date_of_birth=date_of_birth,
                                gender_identity=gender_identity,
                                address_1=address_1,
                                address_2=address_2,
                                city=city,
                                state=state,
                                zipcode=zipcode,
                                phone_number=phone_number,
                                phone_type=phone_type,
                                email=email)
            db.session.add(new_person)
            db.session.commit()
            flash(f'{first_name} {last_name} created successfully.',
                  category='success')

            # Redirect to view people
            return redirect(url_for('views.people'))

    return render_template("add_people.html",
                           title="Soulstone - Add Person",
                           user=current_user,
                           form=form)


# People - Edit Person
@views.route('/person/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editPerson(id):
    form = EditPersonForm()

    person = People.query.get_or_404(id)

    if request.method == 'GET':
        # pre-populate form
        form.first_name.data = person.first_name
        form.middle_name.data = person.middle_name
        form.last_name.data = person.last_name
        form.suffix_name.data = person.suffix_name
        form.date_of_birth.data = person.date_of_birth
        form.gender_identity.data = person.gender_identity
        form.address_1.data = person.address_1
        form.address_2.data = person.address_2
        form.city.data = person.city
        form.state.data = person.state
        form.zipcode.data = person.zipcode
        form.phone.data = person.phone_number
        form.phone_type.data = person.phone_type
        form.email.data = person.email
        form.status.data = person.status

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            person.updated_at = datetime.utcnow()
            person.updated_by = current_user.get_id()
            person.first_name = form.first_name.data
            person.middle_name = form.middle_name.data
            person.last_name = form.last_name.data
            person.suffix_name = form.suffix_name.data
            person.date_of_birth = form.date_of_birth.data
            person.gender_identity = form.gender_identity.data
            person.address_1 = form.address_1.data
            person.address_2 = form.address_2.data
            person.city = form.city.data
            person.state = form.state.data
            person.zipcode = form.zipcode.data
            person.phone_number = form.phone.data
            person.phone_type = form.phone_type.data
            person.email = form.email.data
            person.status = form.status.data

            # Update person to database
            db.session.commit()
            flash(f'{person.first_name} {person.last_name} updated successfully.',
                  category='success')

            return redirect(url_for('views.viewPerson', id=person.id))

    return render_template("edit_person.html",
                           title="Soulstone - Edit Person",
                           user=current_user,
                           person=person,
                           form=form)


# People - View Person
@views.route('/person/<int:id>')
def viewPerson(id):
    if request.method == 'GET':
        # current user practice id
        pu_id = current_user.practice_id
        pp_id = People.query.get_or_404(id).practice_id

        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)

            return render_template("person.html",
                                   user=current_user,
                                   person=person)
        else:
            return render_template("401.html",
                                   user=current_user)


# ------------------------------------------------------------------------------
# Routes - Practice - Notes
# ------------------------------------------------------------------------------
@views.route('/notes')
@login_required
def notes():
    ''' Routes the user to the Notes page '''
    return render_template("notes.html", title="Soulstone - Notes",
                           user=current_user)


@views.route('/notes/add_visit_note', methods=['GET', 'POST'])
@login_required
def addVisitNote():
    form = AddVisitNoteForm()

    person = People.query.first()

    return render_template("add_visit_note.html",
    title="Soulstone - Add Visit Note",
    user=current_user,
    person=person,
    form=form)


# ------------------------------------------------------------------------------
# Routes - Practice - Billing
# ------------------------------------------------------------------------------
@views.route('/billing')
@login_required
def billing():
    ''' Routes the user to the Billing page '''
    return render_template("billing.html", title="Soulstone - Billing",
                           user=current_user)


# ------------------------------------------------------------------------------
# Routes - Practice - Settings
# ------------------------------------------------------------------------------
# View Practice Information
@views.route('/settings/practice_info')
@login_required
def practiceSettings():
    ''' Routes the user to the Settings - Practice Information page '''
    if request.method == 'GET':
        pu_id = current_user.practice_id
        practice = Practice.query.get_or_404(pu_id)

        # Practice counts
        people_count = People.query.filter_by(practice_id=pu_id).count()
        user_count = User.query.filter_by(practice_id=pu_id).count()
        # TODO: visit note count
        # TODO: charges count

        return render_template("settings_practice_info.html",
                               title="Soulstone - Settings - Practice Information",
                               practice=practice,
                               people_count=people_count,
                               user_count=user_count,
                               user=current_user)


# Edit Practice Information
@views.route('/settings/<int:id>/edit_practice_info', methods=['GET', 'POST'])
@login_required
def editPracticeInformation(id):
    ''' Routes the user to edit the practice information '''
    form = EditPracticeForm()

    practice = Practice.query.get_or_404(id)

    if request.method == 'GET':
        # pre-populate form
        form.name.data = practice.name
        form.biography.data = practice.biography
        form.address_1.data = practice.address_1
        form.address_2.data = practice.address_2
        form.city.data = practice.city
        form.state.data = practice.state
        form.zipcode.data = practice.zipcode
        form.phone.data = practice.phone_number
        form.phone_type.data = practice.phone_type
        form.email.data = practice.email
        form.website.data = practice.website

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice.updated_at = datetime.utcnow()
            practice.name = form.name.data
            practice.biography = form.biography.data
            practice.address_1 = form.address_1.data
            practice.address_2 = form.address_2.data
            practice.city = form.city.data
            practice.state = form.state.data
            practice.zipcode = form.zipcode.data
            practice.phone_number = form.phone.data
            practice.phone_type = form.phone_type.data
            practice.email = form.email.data
            practice.website = form.website.data

            # Update person to database
            db.session.commit()
            flash(f'{practice.name} updated successfully.',
                  category='success')

            return redirect(url_for('views.practiceSettings'))

    return render_template("edit_practice.html",
                           title="Soulstone - Edit Practice",
                           user=current_user,
                           practice=practice,
                           form=form)


# View Charges
@views.route('/settings/charges')
@login_required
def chargeSettings():
    ''' Routes the user to the Settings - Charges page '''
    if request.method == 'GET':
        pu_id = current_user.practice_id
        charges = Charges.query.filter_by(practice_id=pu_id).all()

        # Practice counts
        charges_count = Charges.query.filter_by(practice_id=pu_id).count()

        return render_template("settings_charges.html",
                               title="Soulstone - Settings - Charges",
                               charges=charges,
                               charges_count=charges_count,
                               user=current_user)


# Add New Charge
@views.route('/settings/add_charge', methods=['GET', 'POST'])
@login_required
def addCharge():
    ''' Routes user to add a new charge '''
    form = AddChargeForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            code = form.code.data
            name = form.name.data
            description = form.description.data
            amount = request.form.get('amount')
            status = form.status.data

            # Add new charge to database
            new_charge = Charges(practice_id=practice_id,
                                 created_at=created_at,
                                 created_by=created_by,
                                 updated_at=updated_at,
                                 updated_by=updated_by,
                                 code=code,
                                 name=name,
                                 description=description,
                                 amount=amount,
                                 status=status)
            db.session.add(new_charge)
            db.session.commit()
            flash(f'{name} created successfully.',
                  category='success')

            # Redirect to view people
            return redirect(url_for('views.chargeSettings'))

    return render_template("add_charge.html",
                           title="Soulstone - Add Charge",
                           user=current_user,
                           form=form)


# View Charge
@views.route('/settings/charges/<int:id>')
@login_required
def viewCharge(id):
    if request.method == 'GET':
        # current user practice id
        pu_id = current_user.practice_id
        charge_id = Charges.query.get_or_404(id).practice_id

        # check if user practice id matches charge id
        if pu_id == charge_id:
            # Display the charge info
            charge = Charges.query.get_or_404(id)

            return render_template("charge.html",
                                   user=current_user,
                                   charge=charge)
        else:
            return render_template("401.html",
                                   user=current_user)


# Edit Charge
@views.route('/settings/charges/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editCharge(id):
    ''' Routes the user to edit the charge '''
    form = EditChargeForm()

    charge = Charges.query.get_or_404(id)

    if request.method == 'GET':
        # pre-populate form
        form.code.data = charge.code
        form.name.data = charge.name
        form.description.data = charge.description
        form.status.data = charge.status

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            charge.updated_at = datetime.utcnow()
            charge.updated_by = current_user.get_id()
            charge.code = form.code.data
            charge.name = form.name.data
            charge.description = form.description.data
            charge.amount = request.form.get('amount')
            charge.status = form.status.data

            # Update person to database
            db.session.commit()
            flash(f'{charge.name} updated successfully.',
                  category='success')

            return redirect(url_for('views.viewCharge', id=charge.id))

    return render_template("edit_charge.html",
                           title="Soulstone - Edit Charge",
                           user=current_user,
                           charge=charge,
                           form=form)


# ------------------------------------------------------------------------------
# Routes - Support
# ------------------------------------------------------------------------------
# Support - Practices
@views.route('/support')
@login_required
def support():
    if request.method == "GET":
        if current_user.role == "Support":
            practices = Practice.query.order_by(Practice.id).all()

            return render_template("support.html",
                                   user=current_user,
                                   practices=practices)
        else:
            return render_template("401.html",
                                   user=current_user)


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
            address_1 = form.address_1.data
            address_2 = form.address_2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            email = form.email.data
            website = form.website.data
            phone_number = form.phone.data
            phone_type = form.phone_type.data

        # Add new practice to database
        new_practice = Practice(name=name,
                                biography=biography,
                                address_1=address_1,
                                address_2=address_2,
                                city=city,
                                state=state,
                                zipcode=zipcode,
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

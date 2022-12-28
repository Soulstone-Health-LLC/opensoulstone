# soulstone/website/settings/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import random
import string
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from website.settings.forms import AddChargeForm, EditChargeForm
from website.settings.forms import EditPracticeForm, EventTypeForm
from website.settings.forms import PracticeUserForm
from website import db, mail
from website.models import Charges, People, Practice, User, Notes
from website.models import LedgerCharges, EventTypes


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
settings = Blueprint('settings', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Settings
# ------------------------------------------------------------------------------
# View Practice Information
@settings.route('/settings/practice_info')
@login_required
def practiceSettings():
    ''' Routes the user to the Settings - Practice Information page '''
    if request.method == 'GET':
        pu_id = current_user.practice_id
        practice = Practice.query.get_or_404(pu_id)

        # Practice counts
        people_count = People.query.filter_by(practice_id=pu_id).count()
        user_count = User.query.filter_by(practice_id=pu_id).count()
        visit_notes_count = Notes.query.filter_by(practice_id=pu_id).count()
        total_charges = db.session.query(db.func.sum(
            LedgerCharges.units * LedgerCharges.unit_amount + (LedgerCharges.unit_amount * LedgerCharges.tax_rate))).filter_by(practice_id=current_user.practice_id).scalar()

        if total_charges is None:
            total_charges = 0

        return render_template("settings_practice_info.html",
                               title="Soulstone - Settings - Practice Information",
                               practice=practice,
                               people_count=people_count,
                               user_count=user_count,
                               visit_notes_count=visit_notes_count,
                               total_charges=total_charges,
                               user=current_user)


# Edit Practice Information
@settings.route('/settings/<int:id>/edit_practice_info',
                methods=['GET', 'POST'])
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

            return redirect(url_for('settings.practiceSettings'))

    return render_template("edit_practice.html",
                           title="Soulstone - Edit Practice",
                           user=current_user,
                           practice=practice,
                           form=form)


# View Practice Users
@settings.route('/settings/practice_users')
@login_required
def practiceUsers():
    ''' Routes the user to the Settings - Practice Users page '''
    if request.method == 'GET':
        users = User.query.filter_by(
            practice_id=current_user.practice_id).all()

        return render_template("settings_practice_users.html",
                               title="Soulstone - Settings - Practice Users",
                               users=users,
                               user=current_user)


# Add Practice User
@settings.route('/settings/add_practice_user', methods=['GET', 'POST'])
@login_required
def addPracticeUser():
    ''' Routes the user to add a practice user '''
    form = PracticeUserForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            first_name = form.first_name.data
            middle_name = form.middle_name.data
            last_name = form.last_name.data
            suffix_name = form.suffix_name.data
            email = form.email.data
            phone_number = form.phone_number.data
            phone_type = form.phone_type.data
            address_1 = form.address_1.data
            address_2 = form.address_2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data

        # Generate a random password
        rand_password = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=12))

        check_email = User.query.filter_by(email=email).first()
        if check_email:
            # security issue - should look at some better wording
            flash('Email is already in use.', category='error')
        else:
            # Create person
            new_user = User(first_name=first_name,
                            middle_name=middle_name,
                            last_name=last_name,
                            suffix_name=suffix_name,
                            email=email,
                            password=generate_password_hash(
                                rand_password, method='sha256'),
                            phone_number=phone_number,
                            phone_type=phone_type,
                            address_1=address_1,
                            address_2=address_2,
                            city=city,
                            state=state,
                            zipcode=zipcode,
                            practice_id=current_user.practice_id,
                            created_at=datetime.utcnow(),
                            created_by=current_user.get_id())

            # Add person to database
            db.session.add(new_user)
            db.session.commit()
            flash(f'{first_name} {last_name} added successfully.',
                  category='success')

            # send email to new user
            msg = Message('Soulstone - New User',
                          recipients=[email],
                          sender='noreply@soulstone.com')
            msg.body = f'''Hello {first_name},

            Welcome to Soulstone! You have been added as a user to {current_user.practice.name}.

            Your login email is: {email}

            Your temporary password is: {rand_password}

            Please login to Soulstone and change your password.
            {url_for('users.login', _external=True)}'''
            mail.send(msg)

            return redirect(url_for('settings.practiceUsers'))

    return render_template("add_practice_user.html",
                           title="Soulstone - Add Practice User",
                           user=current_user,
                           form=form)


# Edit Practice User
@settings.route('/settings/<int:user_id>/edit_practice_user',
                methods=['GET', 'POST'])
@login_required
def editPracticeUser(user_id):
    ''' Routes the user to edit the practice user '''
    form = PracticeUserForm()

    p_user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        # pre-populate form
        form.first_name.data = p_user.first_name
        form.middle_name.data = p_user.middle_name
        form.last_name.data = p_user.last_name
        form.suffix_name.data = p_user.suffix_name
        form.email.data = p_user.email
        form.phone_number.data = p_user.phone_number
        form.phone_type.data = p_user.phone_type
        form.address_1.data = p_user.address_1
        form.address_2.data = p_user.address_2
        form.city.data = p_user.city
        form.state.data = p_user.state
        form.zipcode.data = p_user.zipcode
        form.role.data = p_user.role
        form.status.data = p_user.status

    if form.validate_on_submit():
        if request.method == 'POST':
            # Update user
            p_user.updated_at = datetime.utcnow()
            p_user.updated_by = current_user.get_id()
            p_user.first_name = form.first_name.data
            p_user.middle_name = form.middle_name.data
            p_user.last_name = form.last_name.data
            p_user.suffix_name = form.suffix_name.data
            p_user.email = form.email.data
            p_user.phone_number = form.phone_number.data
            p_user.phone_type = form.phone_type.data
            p_user.address_1 = form.address_1.data
            p_user.address_2 = form.address_2.data
            p_user.city = form.city.data
            p_user.state = form.state.data
            p_user.zipcode = form.zipcode.data
            p_user.role = form.role.data
            p_user.status = form.status.data

            # Update person to database
            db.session.commit()
            flash(f'{p_user.first_name} {p_user.last_name} updated successfully.',
                  category='success')

            return redirect(url_for('settings.practiceUsers'))

    return render_template("edit_practice_user.html",
                           title="Soulstone - Edit Practice User",
                           user=current_user,
                           p_user=p_user,
                           form=form)


# View Charges
@settings.route('/settings/charges')
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
@settings.route('/settings/add_charge', methods=['GET', 'POST'])
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
            return redirect(url_for('settings.chargeSettings'))

    return render_template("add_charge.html",
                           title="Soulstone - Add Charge",
                           user=current_user,
                           form=form)


# View Charge
@settings.route('/settings/charges/<int:id>')
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
@settings.route('/settings/charges/<int:id>/edit', methods=['GET', 'POST'])
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
        form.amount.data = charge.amount
        form.status.data = charge.status

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            charge.updated_at = datetime.utcnow()
            charge.updated_by = current_user.get_id()
            charge.code = form.code.data
            charge.name = form.name.data
            charge.description = form.description.data
            charge.amount = form.amount.data
            charge.status = form.status.data

            # Update person to database
            db.session.commit()
            flash(f'{charge.name} updated successfully.',
                  category='success')

            return redirect(url_for('settings.viewCharge', id=charge.id))

    return render_template("edit_charge.html",
                           title="Soulstone - Edit Charge",
                           user=current_user,
                           charge=charge,
                           form=form)


# View Event Types
@settings.route('/settings/event_types')
@login_required
def viewEventTypes():
    '''Route to see the list of event types'''
    if request.method == 'GET':
        pu_id = current_user.practice_id
        event_types = EventTypes.query.filter_by(practice_id=pu_id).all()

        # Practice counts
        event_type_count = EventTypes.query.filter_by(
            practice_id=pu_id).count()

        return render_template("settings_event_types.html",
                               title="Soulstone - Settings - Event Types",
                               event_types=event_types,
                               event_type_count=event_type_count,
                               user=current_user)


# Add Event Type
@settings.route('/settings/add_event_type', methods=['GET', 'POST'])
@login_required
def addEventType():
    '''Routes the user to add a new event type'''
    form = EventTypeForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_name = form.event_name.data
            event_description = form.event_description.data
            event_status = form.event_status.data

            # Add new event type to database
            new_event_type = EventTypes(practice_id=practice_id,
                                        created_at=created_at,
                                        created_by=created_by,
                                        updated_at=updated_at,
                                        updated_by=updated_by,
                                        event_name=event_name,
                                        event_description=event_description,
                                        event_status=event_status)
            db.session.add(new_event_type)
            db.session.commit()
            flash(f'{event_name} created successfully.',
                  category='success')
            return redirect(url_for('settings.viewEventTypes'))

    return render_template("add_event_type.html",
                           title="Soulstone - Add Event Type",
                           form=form,
                           user=current_user)


# Edit Event Type
@settings.route('/settings/event_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editEventType(id):
    '''Routes the user to edit the event type'''
    form = EventTypeForm()

    event_type = EventTypes.query.get_or_404(id)

    if request.method == 'GET':
        # pre-populate form
        form.event_name.data = event_type.event_name
        form.event_description.data = event_type.event_description
        form.event_status.data = event_type.event_status

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            event_type.updated_at = datetime.utcnow()
            event_type.updated_by = current_user.get_id()
            event_type.event_name = form.event_name.data
            event_type.event_description = form.event_description.data
            event_type.event_status = form.event_status.data

            # Update event type to database
            db.session.commit()
            flash(f'{event_type.event_name} updated successfully.',
                  category='success')

            return redirect(url_for('settings.viewEventTypes'))

    return render_template("edit_event_type.html",
                           title="Soulstone - Edit Event Type",
                           user=current_user,
                           event_type=event_type,
                           form=form)

# soulstone/website/settings/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.settings.forms import AddChargeForm, EditChargeForm
from website.settings.forms import EditPracticeForm
from website import db
from website.models import Charges, People, Practice, User, Notes, LedgerCharges


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

            return redirect(url_for('settings.viewCharge', id=charge.id))

    return render_template("edit_charge.html",
                           title="Soulstone - Edit Charge",
                           user=current_user,
                           charge=charge,
                           form=form)

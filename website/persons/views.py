# soulstone/website/persons/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.persons.forms import AddPersonForm, EditPersonForm
from website import db
from website.models import People, Notes, Charges, LedgerCharges, LedgerPayments


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
persons = Blueprint('persons', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Persons
# ------------------------------------------------------------------------------
# Persons
@persons.route('/people')
@login_required
def people():
    if request.method == 'GET':
        people = People.query.filter_by(
            practice_id=current_user.practice_id).order_by(People.last_name).all()

    return render_template("people.html",
                           title="Soulstone - People",
                           user=current_user,
                           people=people)


# Persons - Add New Person
@persons.route('/people/add_person', methods=['GET', 'POST'])
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
            return redirect(url_for('persons.people'))

    return render_template("add_people.html",
                           title="Soulstone - Add Person",
                           user=current_user,
                           form=form)


# Persons - Edit Person
@persons.route('/person/<int:id>/edit', methods=['GET', 'POST'])
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

            return redirect(url_for('persons.viewPerson', id=person.id))

    return render_template("edit_person.html",
                           title="Soulstone - Edit Person",
                           user=current_user,
                           person=person,
                           form=form)


# Persons - View Person
@persons.route('/person/<int:id>')
def viewPerson(id):
    if request.method == 'GET':
        # current user practice id
        pu_id = current_user.practice_id
        pp_id = People.query.get_or_404(id).practice_id

        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)
            notes = Notes.query.filter_by(person_id=id).all()
            notes_count = Notes.query.filter_by(person_id=id).count()
            ledger_charges = db.session.query(LedgerCharges.created_at,
                                              LedgerCharges.units,
                                              LedgerCharges.unit_amount,
                                              LedgerCharges.tax_rate,
                                              LedgerCharges.practice_id,
                                              Charges.code,
                                              Charges.description)\
                .filter_by(person_id=id)\
                .join(Charges, LedgerCharges.charge_id == Charges.id).all()
            total_charges = db.session.query(db.func.sum(LedgerCharges.units * LedgerCharges.unit_amount + (
                LedgerCharges.unit_amount * LedgerCharges.tax_rate))).filter_by(practice_id=current_user.practice_id, person_id=id).scalar()
            total_payments = db.session.query(db.func.sum(LedgerPayments.amount)).filter_by(
                practice_id=current_user.practice_id, person_id=id).scalar()

            if total_charges is None:
                total_charges = 0
            if total_payments is None:
                total_payments = 0
            balance = total_charges - total_payments

            return render_template("person.html",
                                   user=current_user,
                                   person=person,
                                   notes=notes,
                                   notes_count=notes_count,
                                   ledger_charges=ledger_charges,
                                   balance=balance)
        else:
            return render_template("401.html",
                                   user=current_user)

"""
Persons > Views - This file contains the views for the Persons Blueprint.
"""

# Imports
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from persons.forms import (
    AddPersonForm,
    EditPersonForm,
    SearchPersonForm,
)
from app import db
from persons.models import People
from visit_notes.models import Notes
from billing.models import Charges, LedgerCharges, LedgerPayments
from events.models import Events, EventTypes
from users.models import User
from persons.person_header import personHeader
from utils.picture_handler import add_profile_pic


# Blueprint Configuration
persons = Blueprint("persons", __name__)


# Persons
@persons.route("/people")
@login_required
def people():
    if request.method == "GET":
        people_list = (
            People.query.filter_by(practice_id=current_user.practice_id)
            .order_by(People.last_name)
            .all()
        )
        people_count = People.query.filter_by(
            practice_id=current_user.practice_id
        ).count()

    return render_template(
        "persons/people.html",
        title="Soulstone - People",
        user=current_user,
        people_list=people_list,
        people_count=people_count,
    )


# Persons - Search
@persons.route("/people/search", methods=["GET", "POST"])
@login_required
def searchPerson():
    """Search for a person"""
    form = SearchPersonForm()
    if form.validate_on_submit():
        if request.method == "POST":
            query = form.query.data
            results = People.query.filter(
                People.first_name.contains(query) |
                People.last_name.contains(query) |
                People.email.contains(query) |
                People.phone_number.contains(query)
            ).all()
            results_count = People.query.filter(
                People.first_name.contains(
                    query) | People.last_name.contains(query)
            ).count()

        return render_template(
            "persons/people_search.html",
            form=form,
            results=results,
            results_count=results_count,
            user=current_user,
        )

    return render_template("persons/people_search.html", form=form,
                           user=current_user)


# Persons - Add New Person
@persons.route("/people/add_person", methods=["GET", "POST"])
@login_required
def addPerson():
    form = AddPersonForm()

    if form.validate_on_submit():
        # Get data from the form
        practice_id = current_user.practice_id
        created_at = datetime.now(tz=timezone.utc)
        created_by = current_user.id
        updated_at = datetime.now(tz=timezone.utc)
        updated_by = current_user.id
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
        # If profile picture is included, save it to the filesystem
        if form.picture.data:
            current_time = datetime.now(tz=timezone.utc)
            formatted_time = current_time.strftime("%Y-%m-%d-%H-%M")
            username = f"{current_user.practice_id}_{
                first_name}_{last_name}_{formatted_time}"
            pic = add_profile_pic(form.picture.data, username)

        # Add new practice to database
        # If a profile picture was uploaded, add it to the database
        if form.picture.data:
            new_person = People(
                practice_id=practice_id,
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
                email=email,
                profile_image=pic,
            )
            db.session.add(new_person)
            db.session.commit()
            flash(
                f"{first_name} {last_name} created successfully.",
                category="success",
            )
        else:
            new_person = People(
                practice_id=practice_id,
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
                email=email,
            )
            db.session.add(new_person)
            db.session.commit()
            flash(
                f"{first_name} {last_name} created successfully.",
                category="success",
            )

        # Redirect to view people
        return redirect(url_for("persons.people"))

    return render_template(
        "persons/add_people.html",
        title="Soulstone - Add Person",
        user=current_user,
        form=form,
    )


# Persons - Edit Person
@persons.route("/person/<int:id>/edit", methods=["GET", "POST"])
@login_required
def editPerson(id):
    form = EditPersonForm()

    person = People.query.get_or_404(id)

    if request.method == "GET":
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
        if request.method == "POST":
            # Get data from the form
            # If profile picture is included, save it to the filesystem
            if form.picture.data:
                current_time = datetime.now(tz=timezone.utc)
                formatted_time = current_time.strftime("%Y-%m-%d-%H-%M")
                username = f"{current_user.practice_id}_{
                    person.first_name}_{person.last_name}_{formatted_time}"
                pic = add_profile_pic(form.picture.data, username)
                person.profile_image = pic
            person.updated_at = datetime.now(tz=timezone.utc)
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
            flash(
                f"""
                {person.first_name} {person.last_name} updated successfully.
                """,
                category="success",
            )

            return redirect(url_for("persons.viewPerson", id=person.id))

    return render_template(
        "persons/edit_person.html",
        title="Soulstone - Edit Person",
        user=current_user,
        person=person,
        form=form,
    )


# Persons - View Person
@persons.route("/person/<int:id>")
def viewPerson(id):
    if request.method == "GET":
        # current user practice id
        pu_id = current_user.practice_id
        pp_id = People.query.get_or_404(id).practice_id

        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)
            # Visit Notes
            notes = Notes.query.filter_by(person_id=id).all()

            # Events
            events = (
                db.session.query(
                    Events.id,
                    Events.date,
                    Events.start_time,
                    Events.end_time,
                    Events.note,
                    User.first_name,
                    User.last_name,
                    EventTypes.event_name,
                )
                .filter_by(person_id=id)
                .outerjoin(User, Events.practitioner_id == User.id)
                .outerjoin(EventTypes, Events.event_type_id == EventTypes.id)
                .all()
            )

            # Ledger Charges
            ledger_charges = (
                db.session.query(
                    LedgerCharges.id,
                    LedgerCharges.created_at,
                    LedgerCharges.units,
                    LedgerCharges.unit_amount,
                    LedgerCharges.tax_rate,
                    LedgerCharges.practice_id,
                    Charges.code,
                    Charges.description,
                )
                .filter_by(person_id=id)
                .join(Charges, LedgerCharges.charge_id == Charges.id)
                .all()
            )

            # Ledger Payments
            ledger_payments = (
                db.session.query(
                    LedgerPayments.id,
                    LedgerPayments.practice_id,
                    LedgerPayments.created_at,
                    LedgerPayments.amount,
                    LedgerPayments.payment_method,
                    LedgerPayments.check_number,
                    LedgerPayments.credit_card_last_four,
                    LedgerPayments.payment_note,
                )
                .filter_by(person_id=id)
                .all()
            )

            # Base Person Header
            person_header, notes_count, events_count, balance = personHeader(
                id)

            return render_template(
                "persons/person.html",
                user=current_user,
                person=person,
                notes=notes,
                ledger_charges=ledger_charges,
                ledger_payments=ledger_payments,
                events=events,
                person_header=person_header,
                notes_count=notes_count,
                events_count=events_count,
                balance=balance,
            )
        else:
            return render_template("error_pages/401.html", user=current_user)

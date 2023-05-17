"""
Support > Views - This file contains the views for the Support Blueprint.
"""

# Imports
import random
import string
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from src.support.forms import AddPracticeForm, PracticeUserForm
from src import db
from src.models import Practice, User
from src.decorators.decorators import support_required


# Blueprint Configuration
supportapp = Blueprint("supportapp", __name__)


# Support - Practices
@supportapp.route("/support")
@login_required
@support_required
def support():

    practices = Practice.query.order_by(Practice.id).all()

    return render_template(
        "support/support.html", user=current_user, practices=practices
    )


# Support - Practices - View Practice
@supportapp.route("/support/<int:id>")
@login_required
@support_required
def viewpractice(id):
    practice = Practice.query.get_or_404(id)
    practice_user = User.query.order_by(User.last_name).all()
    return render_template(
        "support/support_practice.html",
        user=current_user,
        practice=practice,
        practice_user=practice_user,
    )


# Support - Practices - Add Practice
@supportapp.route("/support/add_practice", methods=["GET", "POST"])
@login_required
@support_required
def addpractice():
    """Add practice form and page"""
    form = AddPracticeForm()

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
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
        new_practice = Practice(
            name=name,
            biography=biography,
            address_1=address_1,
            address_2=address_2,
            city=city,
            state=state,
            zipcode=zipcode,
            email=email,
            website=website,
            phone_number=phone_number,
            phone_type=phone_type,
        )
        db.session.add(new_practice)
        db.session.commit()
        flash(f"{name} created successfully.", category="success")

        # Redirect user to the Support home page
        return redirect(url_for("views.support"))

    return render_template(
        "support/add_practice.html",
        title="Soulstone - Add Practice",
        form=form,
        user=current_user,
    )


# Support - Practices - Add Practice User
@supportapp.route("/support/<int:id>/support_add_user",
                  methods=["GET", "POST"])
@login_required
@support_required
def addPracticeUser(id):
    """Add practice user form and page"""
    form = PracticeUserForm()
    practice = Practice.query.get(id)

    # Random string
    def randompass(length):
        """Generates a random string for a temporary password"""
        s = string
        letters = s.ascii_lowercase + s.ascii_uppercase + s.digits
        return "".join(random.choice(letters) for i in range(length))

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            practice_id = request.form.get("practice_id")
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
            new_practice_user = User(
                practice_id=practice_id,
                role=role,
                first_name=firstname,
                middle_name=middlename,
                last_name=lastname,
                suffix_name=suffix,
                email=email,
                password=generate_password_hash(password, method="sha384"),
                phone_number=phonenumber,
                phone_type=phonetype,
                status="Active",
            )
            db.session.add(new_practice_user)
            db.session.commit()
            flash(f"{form.email} created successfully.", category="success")

            # Redirect user to Support home page
            return redirect(url_for("supportapp.support"))

    return render_template(
        "support/support_add_user.html",
        title="Soulstone - Add Practice User",
        user=current_user,
        form=form,
        practice=practice,
    )

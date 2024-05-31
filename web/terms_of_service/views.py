"""Terms of Service - User Agreement View"""
# Imports
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from decorators.decorators import support_required
from app import db
from .controls import get_tos_details
from .forms import UserAgreementForm, TermsOfServiceForm
from .models import UserAgreement, TermsOfService


# Blueprint Configuration
terms_of_service = Blueprint("terms_of_service", __name__)


# User Agreement Page
@terms_of_service.route("/terms_of_service/<int:tos_id>",
                        methods=["GET", "POST"])
@login_required
def user_agreement(tos_id):
    """User Agreement page"""

    form = UserAgreementForm()
    agreement_content = TermsOfService.query.filter_by(id=tos_id).first()

    # If user clicks "I Agree"
    if form.validate_on_submit():
        # Save user agreement to database
        user_agreement_signed = UserAgreement(
            user_id=current_user.id,
            tos_id=tos_id,
            agreed_date=datetime.now(tz=timezone.utc),
        )
        db.session.add(user_agreement_signed)
        db.session.commit()

        # Redirect user to home page
        return redirect(url_for("core.home"))

    return render_template(
        "terms_of_service/user_agreement.html",
        form=form, agreement_content=agreement_content
    )


# Support - Terms of Service - List Terms of Service
@terms_of_service.route("/support/terms_of_service", methods=["GET"])
@login_required
@support_required
def support_list_tos():
    """Support - Terms of Service - List Terms of Service"""

    # Get all terms of service
    tos = TermsOfService.query.all()

    return render_template(
        "terms_of_service/support_list_tos.html", user=current_user, tos=tos
    )


# Support - Terms of Service - View Terms of Service
@terms_of_service.route("/support/terms_of_service/<int:tos_id>",
                        methods=["GET"])
@login_required
@support_required
def support_view_tos(tos_id):
    """Support - Terms of Service - View Terms of Service"""

    # Get terms of service details
    tos = get_tos_details(tos_id)

    return render_template(
        "terms_of_service/support_view_tos.html", tos=tos
    )


# Support - Terms of Service - Create Terms of Service
@terms_of_service.route("/support/terms_of_service/create",
                        methods=["GET", "POST"])
@login_required
@support_required
def support_create_tos():
    """Support - Terms of Service - Create Terms of Service"""

    form = TermsOfServiceForm()

    # If form is submitted
    if form.validate_on_submit():
        new_tos = TermsOfService()
        form.populate_obj(new_tos)
        new_tos.created_by = current_user.id
        db.session.add(new_tos)
        db.session.commit()
        flash("Terms of Service created successfully.", category="success")

        # Redirect user to support - list terms of service page
        return redirect(url_for("terms_of_service.support_list_tos"))

    return render_template(
        "terms_of_service/support_add_edit_tos.html",
        title="Create Terms of Service", form=form
    )


# Support - Terms of Service - Edit Terms of Service
@terms_of_service.route(
    "/support/terms_of_service/edit/<int:tos_id>", methods=["GET", "POST"]
)
@login_required
@support_required
def support_edit_tos(tos_id):
    """Support - Terms of Service - Edit Terms of Service"""

    tos = TermsOfService.query.filter_by(id=tos_id).first()
    form = TermsOfServiceForm(obj=tos)

    if form.validate_on_submit():
        form.populate_obj(tos)
        tos.updated_date = datetime.now(tz=timezone.utc)
        tos.updated_by = current_user.id
        db.session.commit()
        flash("Terms of Service updated successfully.", category="success")

        # Redirect user to support - list terms of service page
        return redirect(url_for("terms_of_service.support_list_tos"))

    return render_template(
        "terms_of_service/support_add_edit_tos.html",
        title="Soulstone - Edit Terms of Service", form=form
    )

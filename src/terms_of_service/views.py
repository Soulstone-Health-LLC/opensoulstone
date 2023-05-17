"""
Terms of Service - User Agreement View
"""

# Imports
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime
from src.terms_of_service.forms import UserAgreementForm
from src.models import UserAgreement, TermsOfService
from src import db
from src.decorators.decorators import support_required


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
        if request.method == "POST":
            # Get current date and time
            date_time = datetime.now()

            # Save user agreement to database
            user_agreement = UserAgreement(
                user_id=current_user.id,
                tos_id=tos_id,
                agreed_date=date_time,
            )
            db.session.add(user_agreement)
            db.session.commit()

            # Redirect user to home page
            return redirect(url_for("core.home"))

    return render_template("terms_of_service/user_agreement.html",
                           form=form,
                           user=current_user,
                           agreement_content=agreement_content)


# Support - Terms of Service - List Terms of Service
@terms_of_service.route("/support/terms_of_service", methods=["GET"])
@login_required
@support_required
def support_list_tos():
    """Support - Terms of Service - List Terms of Service"""

    # Get all terms of service
    tos = TermsOfService.query.all()

    return render_template("terms_of_service/support_list_tos.html",
                           user=current_user,
                           tos=tos)


# Support - Terms of Service - View Terms of Service
@terms_of_service.route("/support/terms_of_service/<int:tos_id>",
                        methods=["GET"])
@login_required
@support_required
def support_view_tos(tos_id):
    """Support - Terms of Service - View Terms of Service"""

    # Get terms of service
    tos = TermsOfService.query.filter_by(id=tos_id).first()

    return render_template("terms_of_service/support_view_tos.html",
                           user=current_user,
                           tos=tos)

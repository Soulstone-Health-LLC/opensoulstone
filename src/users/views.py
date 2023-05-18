"""
Users > Views - This file contains all of the views for the Users Blueprint.
"""

# Imports
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from src.users.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordForm,
    ResetRequestForm,
)
from src.models import User, TermsOfService, UserAgreement
from src import db, mail


# Blueprint Configuration
users = Blueprint("users", __name__)


# Login Page
@users.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    # If user is currently logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for("core.home"))

    # Login logic
    form = LoginForm()

    # Gets the data from the form and saves as variables
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            password = form.password.data

            # Checks if the user's email is on file
            user = User.query.filter_by(email=email).first()

            # Checks if the password is correct
            if user:
                if check_password_hash(user.password, password):
                    # Check if user is a Support user
                    if user.role == "Support":
                        flash("Logged in successfully", category="success")
                        login_user(user, remember=True)
                        return redirect(url_for("supportapp.support"))
                    else:
                        # Check if password needs to be updated
                        if user.password_reset_by_system:
                            flash("Please update your password.",
                                  category="error")
                            login_user(user, remember=True)
                            return redirect(url_for("users.change_password"))
                        else:
                            # Check if user has agreed to the latest TOS
                            active_tos = TermsOfService.query.filter(
                                TermsOfService.active_date <= datetime.now(),
                                TermsOfService.sunset_date > datetime.now())\
                                .order_by(TermsOfService.active_date.desc())\
                                .first()

                            user_agreement = UserAgreement.query.filter(
                                UserAgreement.user_id == user.id,
                                UserAgreement.tos_id == active_tos.id).first()

                            if not user_agreement:
                                login_user(user, remember=True)
                                return redirect(
                                    url_for("terms_of_service.user_agreement",
                                            tos_id=active_tos.id))
                            else:
                                flash("Logged in successfully",
                                      category="success")
                                login_user(user, remember=True)
                                return redirect(url_for("core.home"))
                else:
                    flash(
                        f"""
                        The account information used for {form.email.data}
                        is incorrect""",
                        category="error",
                    )
            else:
                flash(
                    f"Account not found for {form.email.data}.",
                    category="error")

    return render_template(
        "users/login.html", title="Soulstone - Login", form=form,
        user=current_user
    )


# Forgot Password
def send_mail(user):
    """Generates a serialized token and sends the link to the user's email"""
    token = User.get_token(user)
    msg = Message(
        "Soulstone - Password Reset Request",
        recipients=[user.email],
        sender="noreply@soulstone.com",
    )
    msg.body = f""" To reset your password, please follow the link below:

    {url_for('users.reset_token', token=token, _external=True)}

    If you did not send a password reset request, please ignore this email.

    ...
    """
    mail.send(msg)


# Reset Request Page
@users.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    """Reset page"""
    form = ResetRequestForm()

    if request.method == "POST":
        # Checks if the user's email is on file
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_mail(user)
            flash(
                f"An email to {form.email.data} with a reset password link.",
                category="success",
            )
        else:
            flash(
                f"Account not found with {form.email.data}", category="error")

    return render_template(
        "users/reset_request.html",
        title="Soulstone - Password Reset Request",
        form=form,
    )


# Reset Password Page
@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Checks the link the user clicked and if the token matches"""
    user = User.verify_token(token)
    if user is None:
        flash(
            """That is an invalid token or the token has expired.
              Please try again.""",
            category="error",
        )
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, method="sha256")

        # Update password on database
        user.password = password
        db.session.commit()
        flash(" Password updated!", category="success")
        return redirect(url_for("users.login"))

    return render_template("users/change_password.html", form=form)


# Logout
@users.route("/logout")
@login_required
def logout():
    """Logout operation"""
    logout_user()
    flash("Logged out successfully.", category="success")
    return redirect(url_for("users.login"))


# Sign Up Page
@users.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """Sign up page"""
    form = RegistrationForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data

            # Checks if email already exists
            user = User.query.filter_by(email=email).first()

            if user:
                # security issue - should look at some better wording
                flash("Email is already in use.", category="error")
            else:
                # Add new user to database
                new_user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    user_type="Owner"
                )
                db.session.add(new_user)
                db.session.commit()

                # Flash success message
                flash("Account created!", category="success")

                # Remember the newly registered user
                login_user(new_user, remember=True)

                # redirect the user to landing page
                return redirect(url_for("core.home"))

    return render_template(
        "users/sign_up.html", title="Soulstone - Register", form=form,
        user=current_user
    )


# Change Password Page
@users.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password page"""

    form = ResetPasswordForm()

    if form.validate_on_submit():
        if request.method == "POST":
            password = generate_password_hash(
                form.password.data, method="sha256")

            # Update password on database
            current_user.password = password
            current_user.password_reset_by_system = False
            current_user.password_reset_at = datetime.utcnow()
            current_user.updated_at = datetime.utcnow()
            current_user.updated_by = current_user.id
            db.session.commit()
            flash("Password updated!", category="success")

            # Sent email to user informing password was changed
            msg = Message(
                "Soulstone - Password Changed",
                recipients=[current_user.email],
                sender="noreply@soulstone.com",
            )
            msg.body = f"""
            Your password was changed on
            {current_user.password_reset_at.strftime('%Y-%m-%d %I:%M:%S %p')}
            by {current_user.first_name} {current_user.last_name}.
            
            If you did not change your password,
            please your practice's Super User immediately.
            
            
            You can also reset your password by clicking the link below:
            {url_for('users.reset_request', _external=True)}
            """
            mail.send(msg)

            return redirect(url_for("users.logout"))

    return render_template("users/change_password.html", form=form,
                           user=current_user)

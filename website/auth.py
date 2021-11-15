'''
    File name: auth.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from .forms import RegistrationForm, LoginForm
from .models import User
from . import db, mail


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
auth = Blueprint('auth', __name__)


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
# Login Page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Login page'''
    # Gets the data from the form and saves as variables
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Checks if the user's email is on file
        user = User.query.filter_by(email=email).first()
        # Checks if the password is correct
        if user:
            if check_password_hash(user.password, password):
                print('logged in')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print('password wrong')
        else:
            print('email not found')

    return render_template("login.html", user=current_user)


# Forgot Password
def send_mail(user):
    ''' Generates a serialized token and sends the link to the user's email '''
    token = User.get_token(user)
    msg = Message('Soulstone - Password Reset Request',
                  recipients=[user.email],
                  sender='noreply@soulstone.com')
    msg.body = f''' To reset your password, please follow the link below:

    {url_for('auth.reset_token', token=token, _external=True)}

    If you did not send a password reset request, please ignore this email.

    ...
    '''
    mail.send(msg)


# Reset Request Page
@auth.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    '''Reset page'''
    if request.method == 'POST':
        email = request.form.get('email')
        # Checks if the user's email is on file
        user = User.query.filter_by(email=email).first()
        # Checks if the email exists
        if user:
            send_mail(user)
        else:
            print('email not found')
            flash('Email not found.', category='error')
    return render_template("reset_request.html")


# Reset Password Page
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    ''' Checks the link the user clicked and if the token matches '''
    user_token = User.verify_token(token)
    if user_token is None:
        flash('''That is an invalid token or the token has expired.
              Please try again.''',
              category='error')
        return redirect(url_for('view.reset_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')

        if password != password_repeat:
            flash(' Passwords don\'t match.', category='error')
        else:
            # Update password on database
            update_password = User(
                password=generate_password_hash(password, method='sha384'))
            db.session.execute(update_password)
            db.session.commit()
            flash(' Password updated!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("change_password.html")


# Logout
@auth.route('/logout')
@login_required
def logout():
    '''Logout operation'''
    logout_user()
    flash(' Logged out successfully.', category='success')
    return redirect(url_for('auth.login'))


# Sign Up Page
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    '''Sign up page'''
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data

            # Checks if email already exists
            user = User.query.filter_by(email=email).first()

            if user:
                # security issue - should look at some better wording
                flash('Email is already in use.', category='error')
            else:
                # Add new user to database
                new_user = User(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                password=generate_password_hash(password,
                                                                method='sha384'))
                db.session.add(new_user)
                db.session.commit()

                # Flash success message
                flash(' Account created!', category='success')

                # Remember the newly registered user
                login_user(new_user, remember=True)

                # redirect the user to landing page
                return redirect(url_for('views.home'))
    return render_template("sign_up.html",
                           title="Soulstone - Register",
                           form=form,
                           user=current_user)

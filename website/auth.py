'''
    File name: auth.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db, mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message


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
    token = User.get_token(user)
    msg = Message('Soulstone - Password Reset Request', recipients=[User.email],
                  sender='noreply@soulstone.com')
    msg.body = f''' To reset your password, please follow the link below:
    
    {url_for('auth.reset_token', token=token, _external=True)}
    
    If you did not send a password reset request, please ignore this email.
    
    ...
    '''

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
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid token or the token has expired. Please try again.', category='error')
        return redirect(url_for('view.reset_request'))
    else:
        if request.method == 'POST':
            password = request.form.get('password')
            password_repeat = request.form.get('password_repeat')
            
            if password != password_repeat:
                flash(' Passwords don\'t match.', category='error')
            else:
                # Add new user to database
                update_password = User(password=generate_password_hash(password,
                                                                method='sha384'))
                db.session.add(update_password)
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
    # Gets the data from the form and saves as variables
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        
        # Checks if email already exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # TODO security issue - should look at some better wording
            flash(' Email is already in use.', category='error')
        # Validation logic for the submit form
        elif password != password_repeat:
            flash(' Passwords don\'t match.', category='error')
        else:
            # Add new user to database
            new_user = User(email=email, first_name=firstname,
                            last_name=lastname,
                            password=generate_password_hash(password,
                                                            method='sha384'),
                            practice_id=1)
            db.session.add(new_user)
            db.session.commit()
            flash(' Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

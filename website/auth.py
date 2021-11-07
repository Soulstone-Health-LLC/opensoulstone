'''
    File name: auth.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return render_template("login.html")

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        
        if password != password_repeat:
            flash('The passwords must match', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=firstname, last_name=lastname, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")

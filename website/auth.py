'''
    File name: auth.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return render_template("login.html")

@auth.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

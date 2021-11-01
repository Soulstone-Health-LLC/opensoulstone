'''
    File name: auth.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

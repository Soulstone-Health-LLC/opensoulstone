'''
    File name: __init__.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Flask


# ------------------------------------------------------------------------------
# Read Secret Key from the secretkey.txt file
# ------------------------------------------------------------------------------
def read_secret_key():
    '''Open text file, read the secret key and returns it'''
    with open("secretkey.txt", "r") as r:
        lines = r.readlines()
        return lines[0].strip()


secret_key = read_secret_key()


# ------------------------------------------------------------------------------
# Application initialization
# ------------------------------------------------------------------------------
def create_app():
    '''Initializes  the application using Flask'''
    app = Flask(__name__)
    # Flask secret key configuration
    app.config['SECRET_KEY'] = secret_key

    return app

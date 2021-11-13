'''
    File name: __init__.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail


# ------------------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------------------
db = SQLAlchemy()
DB_NAME = "database.db"

mail = Mail()


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
# Read Secret Key from the secretkey.txt file
# ------------------------------------------------------------------------------
def read_email_password():
    '''Open text file, read the secret key and returns it'''
    with open("emailpassword.txt", "r") as r:
        lines = r.readlines()
        return lines[0].strip()


email_password = read_email_password()


# ------------------------------------------------------------------------------
# Application initialization
# ------------------------------------------------------------------------------
def create_app():
    '''Initializes  the application using Flask'''
    app = Flask(__name__)
    # Flask secret key configuration
    app.config['SECRET_KEY'] = secret_key
    # Flask and SQLAlchemy database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import views and auth routes
    from .views import views
    from .auth import auth

    # Blueprint routing
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Check if database exists; if not, create database and tables (as classes)
    from .models import User
    create_database(app)

    # Initializes the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u'You have to login to view this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'rodneygauna@gmail.com'
    app.config['MAIL_PASSWORD'] = email_password
    mail.init_app(app)

    return app


# ------------------------------------------------------------------------------
# Database initialization
# ------------------------------------------------------------------------------
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')

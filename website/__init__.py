# soulstone/website/__init__.py


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import imp
from flask import Flask, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from os import path


# ------------------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------------------
db = SQLAlchemy()
DB_NAME = "database.db"


# ------------------------------------------------------------------------------
# Mail configuration
# ------------------------------------------------------------------------------
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
# Read email password from the emailpassword.txt file
# ------------------------------------------------------------------------------
def read_email_password():
    '''Open text file, read the email password for Gmail and returns it'''
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
    from website.core.views import core
    from website.users.views import users
    from website.persons.views import persons
    from website.visit_notes.views import visit_notes
    from website.billing.views import billing
    from website.settings.views import settings
    from website.support.views import supportapp
    from website.error_pages.handler import error_pages

    # Blueprint routing
    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(persons)
    app.register_blueprint(visit_notes)
    app.register_blueprint(billing)
    app.register_blueprint(settings)
    app.register_blueprint(supportapp)
    app.register_blueprint(error_pages)

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

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.login'))

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

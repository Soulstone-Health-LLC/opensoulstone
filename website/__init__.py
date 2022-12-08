'''
This file initializes the application using Flask.
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from flask import Flask, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


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
# Read Secret Key and Email Password from .env file
# ------------------------------------------------------------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# ------------------------------------------------------------------------------
# Application initialization
# ------------------------------------------------------------------------------
def create_app():
    '''Initializes  the application using Flask'''
    app = Flask(__name__)
    # Flask secret key configuration
    app.config['SECRET_KEY'] = SECRET_KEY
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
    login_manager.login_view = 'users.login'
    login_manager.login_message = u'You have to login to view this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('users.login'))

    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'rodneygauna@gmail.com'
    app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
    mail.init_app(app)

    return app


# ------------------------------------------------------------------------------
# Database initialization
# ------------------------------------------------------------------------------
def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')

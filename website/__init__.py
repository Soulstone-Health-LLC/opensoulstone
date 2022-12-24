'''
This file initializes the application using Flask.
'''


# Imports
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Read Secret Key and Email Password from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Flask initialization
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the database
db = SQLAlchemy(app)

# Initializes the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Mail configuration and initialization
mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rodneygauna@gmail.com'
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
mail.init_app(app)


# Blueprint routing
from website.core.views import core
from website.calendar.views import calendar
from website.users.views import users
from website.persons.views import persons
from website.visit_notes.views import visit_notes
from website.billing.views import billing
from website.settings.views import settings
from website.support.views import supportapp
from website.error_pages.handler import error_pages
from website.cli.cli_commands import commands

app.register_blueprint(core)
app.register_blueprint(calendar)
app.register_blueprint(users)
app.register_blueprint(persons)
app.register_blueprint(visit_notes)
app.register_blueprint(billing)
app.register_blueprint(settings)
app.register_blueprint(supportapp)
app.register_blueprint(error_pages)
app.register_blueprint(commands)

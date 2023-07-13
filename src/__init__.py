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
SQLITE_LOCATION = os.getenv(
    "SQLITE_LOCATION", os.path.abspath(os.path.dirname(__file__))
)

# Flask initialization
app = Flask(__name__)
basedir = SQLITE_LOCATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
from src.core.views import core
from src.dashboard.views import dashboard
from src.reports.views import reports
from src.calendar.views import calendar
from src.users.views import users
from src.persons.views import persons
from src.visit_notes.views import visit_notes
from src.billing.views import billing
from src.settings.views import settings
from src.support.views import supportapp
from src.error_pages.handler import error_pages
from src.cli.cli_commands import commands
from src.terms_of_service.views import terms_of_service

app.register_blueprint(core)
app.register_blueprint(dashboard)
app.register_blueprint(reports)
app.register_blueprint(calendar)
app.register_blueprint(users)
app.register_blueprint(persons)
app.register_blueprint(visit_notes)
app.register_blueprint(billing)
app.register_blueprint(settings)
app.register_blueprint(supportapp)
app.register_blueprint(error_pages)
app.register_blueprint(commands)
app.register_blueprint(terms_of_service)

"""Flask application initialization and configuration."""
# Imports
from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import BaseConfig


# Flask app configuration
app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)


# Importing the models to create the tables
from billing.models import *
from events.models import *
from persons.models import *
from support.models import *
from terms_of_service.models import *
from users.models import *
from settings.models import *
from visit_notes.models import *


# Login manager initialization
from login_config import login_manager
login_manager.init_app(app)
login_manager.login_view = 'users.login'


# Mail configuration and initialization
mail = Mail(app)
mail.init_app(app)


# Flask Blueprints - Imports
from core.views import core
from dashboard.views import dashboard
from reports.views import reports
from events.views import events
from users.views import users
from persons.views import persons
from visit_notes.views import visit_notes
from billing.views import billing
from settings.views import settings
from support.views import supportapp
from error_pages.handler import error_pages
from terms_of_service.views import terms_of_service
from utils.test_data import commands

# Flask Blueprints - Register
app.register_blueprint(core)
app.register_blueprint(dashboard)
app.register_blueprint(reports)
app.register_blueprint(events)
app.register_blueprint(users)
app.register_blueprint(persons)
app.register_blueprint(visit_notes)
app.register_blueprint(billing)
app.register_blueprint(settings)
app.register_blueprint(supportapp)
app.register_blueprint(error_pages)
app.register_blueprint(terms_of_service)
app.register_blueprint(commands)


# Main function
if __name__ == "__main__":
    app.run(debug=True)

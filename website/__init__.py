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
from models import User, Practice, People

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
from website.users.views import users
from website.persons.views import persons
from website.visit_notes.views import visit_notes
from website.billing.views import billing
from website.settings.views import settings
from website.support.views import supportapp
from website.error_pages.handler import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(persons)
app.register_blueprint(visit_notes)
app.register_blueprint(billing)
app.register_blueprint(settings)
app.register_blueprint(supportapp)
app.register_blueprint(error_pages)


# Flask CLI commands
@app.cli.command('db_create')
def db_create():
    '''Use "flask db_create" to create the database in the terminal'''
    db.create_all()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    '''Use "flask db_drop" to drop the database in the terminal'''
    db.drop_all()
    print('Databased dropped')


@app.cli.command('db_seed')
def db_seed():
    '''Preloads the database with data'''
    support_practice = Practice(name='Support Practice',
                                email='support@email.com',
                                website='www.support.com',
                                phone_number='5555555555',
                                phone_type='Office',
                                address_1='123 Main St',
                                address_2='Suite 100',
                                city='San Francisco',
                                state='CA',
                                zipcode='94105',
                                status='Active')
    test_practice = Practice(name='Test Practice',
                             email='test@email.com',
                             website='www.test.com',
                             phone_number='5555555555',
                             phone_type='Office',
                             address_1='123 Main St',
                             address_2='Suite 100',
                             city='San Francisco',
                             state='CA',
                             zipcode='94105',
                             status='Active')
    support_user = User(practice_id=1,
                        email='rodneygauna+support@gmail.com',
                        password=generate_password_hash('rodneygauna+support', method='sha256'),
                        first_name='Support',
                        last_name='User',
                        role='Support',
                        status='Active')
    test_user = User(practice_id=2,
                        email='rodneygauna+hh@gmail.com',
                        password=generate_password_hash('rodneygauna+hh', method='sha256'),
                        first_name='Rodney',
                        last_name='Gauna',
                        role='Owner',
                        status='Active')
    db.session.add(support_practice)
    print('Added Support Practice')
    db.session.add(test_practice)
    print('Added Test Practice')
    db.session.add(support_user)
    print('Added Support User')
    db.session.add(test_user)
    print('Added Test User')
    print('Database seeded')
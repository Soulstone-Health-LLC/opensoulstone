'''
CLI Commands for the website app
'''

# Imports
from flask import Blueprint
from werkzeug.security import generate_password_hash
from website.models import Practice, User
from .. import db

# Blueprint Configuration
commands = Blueprint('commands', __name__)


# Flask CLI commands
@commands.cli.command('db_create')
def db_create():
    '''Use "flask db_create" to create the database in the terminal'''
    db.create_all()
    print('Database created')


@commands.cli.command('db_drop')
def db_drop():
    '''Use "flask db_drop" to drop the database in the terminal'''
    db.drop_all()
    print('Databased dropped')


@commands.cli.command('db_seed')
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
                        password=generate_password_hash(
                            'rodneygauna+support', method='sha256'),
                        first_name='Support',
                        last_name='User',
                        role='Support',
                        status='Active')
    test_user = User(practice_id=2,
                     email='rodneygauna+hh@gmail.com',
                     password=generate_password_hash(
                         'rodneygauna+hh', method='sha256'),
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

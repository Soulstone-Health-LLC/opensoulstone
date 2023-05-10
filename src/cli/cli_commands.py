'''
CLI Commands for the website app
'''

# Imports
import random
from flask import Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from src.models import Practice, User, People, LedgerCharges, Charges
from src.models import EventTypes
from src import db

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
    # Data to seed the database with
    data = []

    # Support practice
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

    # Test practice
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

    # Support user
    support_user = User(practice_id=1,
                        email='rodneygauna+support@gmail.com',
                        password=generate_password_hash(
                            'rodneygauna+support', method='sha256'),
                        first_name='Support',
                        last_name='User',
                        role='Support',
                        status='Active')

    # Test user
    test_user = User(practice_id=2,
                     email='rodneygauna+hh@gmail.com',
                     password=generate_password_hash(
                         'rodneygauna+hh', method='sha256'),
                     first_name='Rodney',
                     last_name='Gauna',
                     role='Owner',
                     status='Active')

    # Test practice charges
    for i in range(1, 11):
        data.append(Charges(practice_id=2,
                            code=f'TestCharge{i}',
                            name=f'Test Charge {i}',
                            description=f'Test Charge {i} Description',
                            amount=round(random.uniform(1.00, 1000.00)),
                            status='Active'))

    # Test Event Types
    for i in range(1, 11):
        data.append(EventTypes(practice_id=2,
                               event_name=f'Test Event Type {i}',
                               event_description=f'Test Event Type {i} Description',
                               event_status='Active'))

    # Test practice persons
    for i in range(1, 1100):
        data.append(People(practice_id=2,
                           first_name=f'Test {i}',
                           middle_name='Test',
                           last_name=f'Test {i}',
                           suffix_name='Test',
                           address_1='123 Main St',
                           address_2='Suite 100',
                           city='San Francisco',
                           state='CA',
                           zipcode='94105',
                           phone_number=random.randint(1000000000, 9999999999),
                           phone_type='Mobile',
                           email=f'test{i}@soulstone.com',
                           status='Active',
                           gender_identity='She/Her'))

    # Add to the database
    db.session.add(support_practice)
    db.session.add(test_practice)
    db.session.add(support_user)
    db.session.add(test_user)

    for entry in data:
        db.session.add(entry)

    db.session.commit()
    print('Database seeded')

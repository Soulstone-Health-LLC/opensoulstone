'''
CLI Commands for the website app
'''

# Imports
from flask import Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from src.models import Practice, User, People, LedgerCharges, Charges
from src.models import EventTypes
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


@commands.cli.command('db_seed_min')
def db_seed_min():
    '''Preloads the database with data'''
    data = []
    # Support practice
    data.append(Practice(name='Support Practice',
                         email='support@email.com',
                         website='www.support.com',
                         phone_number='5555555555',
                         phone_type='Office',
                         address_1='123 Main St',
                         address_2='Suite 100',
                         city='San Francisco',
                         state='CA',
                         zipcode='94105',
                         status='Active'))
    # Test practice
    data.append(Practice(name='Test Practice',
                         email='test@email.com',
                         website='www.test.com',
                         phone_number='5555555555',
                         phone_type='Office',
                         address_1='123 Main St',
                         address_2='Suite 100',
                         city='San Francisco',
                         state='CA',
                         zipcode='94105',
                         status='Active'))
    # Support user
    data.append(User(practice_id=1,
                     email='rodneygauna+support@gmail.com',
                     password=generate_password_hash(
                         'rodneygauna+support', method='sha256'),
                     first_name='Support',
                     last_name='User',
                     role='Support',
                     status='Active'))
    # Test user
    data.append(User(practice_id=2,
                     email='rodneygauna+hh@gmail.com',
                     password=generate_password_hash(
                         'rodneygauna+hh', method='sha256'),
                     first_name='Rodney',
                     last_name='Gauna',
                     role='Owner',
                     status='Active'))
    # Test clients
    data.append(People(practice_id=1,
                       first_name='John',
                       last_name='Doe',
                       phone_number='5555555555',
                       phone_type='Mobile',))
    data.append(People(practice_id=1,
                       first_name='Jane',
                       last_name='Doe',
                       phone_number='5555555555',
                       phone_type='Mobile',))
    # Test Billing
    data.append(LedgerCharges(created_at=datetime.now(),
                              practice_id=1,
                              charge_id=1,
                              units=1,
                              unit_amount=222,
                              tax_rate=0,
                              created_by=1,
                              person_id=1))
    data.append(LedgerCharges(created_at=datetime.now(),
                              practice_id=1,
                              units=1,
                              charge_id=1,
                              unit_amount=333,
                              tax_rate=0,
                              created_by=1,
                              person_id=1))
    # Test charges
    data.append(Charges(
        practice_id=1,
        code='CHIZ',
        created_by=1,
        name='Chiz',
        description='Chiz Description',
        amount=100.00,
        status='Active'))
    # Add to the database
    for entry in data:
        db.session.add(entry)
    db.session.commit()
    print('Database seeded')


@commands.cli.command('db_seed_max')
def db_seed_max():
    '''Preloads the database with data'''
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
    test_charge_1 = Charges(practice_id=2,
                            code='TestCharge1',
                            name='Test Charge 1',
                            description='Test Charge 1 Description',
                            amount=100.00,
                            status='Active')
    test_charge_2 = Charges(practice_id=2,
                            code='TestCharge2',
                            name='Test Charge 2',
                            description='Test Charge 2 Description',
                            amount=200.00,
                            status='Active')
    # Test Event Types
    test_event_type_1 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 1',
                                   event_description='Test Event Type 1 Description',
                                   event_status='Active')
    test_event_type_2 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 2',
                                   event_description='Test Event Type 2 Description',
                                   event_status='Active')
    test_event_type_3 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 3',
                                   event_description='Test Event Type 3 Description',
                                   event_status='Active')
    test_event_type_4 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 4',
                                   event_description='Test Event Type 4 Description',
                                   event_status='Active')
    test_event_type_5 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 5',
                                   event_description='Test Event Type 5 Description',
                                   event_status='Active')
    test_event_type_6 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 6',
                                   event_description='Test Event Type 6 Description',
                                   event_status='Active')
    test_event_type_7 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 7',
                                   event_description='Test Event Type 7 Description',
                                   event_status='Active')
    test_event_type_8 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 8',
                                   event_description='Test Event Type 8 Description',
                                   event_status='Active')
    test_event_type_9 = EventTypes(practice_id=2,
                                   event_name='Test Event Type 9',
                                   event_description='Test Event Type 9 Description',
                                   event_status='Active')
    test_event_type_10 = EventTypes(practice_id=2,
                                    event_name='Test Event Type 10',
                                    event_description='Test Event Type 10 Description',
                                    event_status='Active')
    test_event_type_11 = EventTypes(practice_id=2,
                                    event_name='Test Event Type 11',
                                    event_description='Test Event Type 11 Description',
                                    event_status='Active')
    test_event_type_12 = EventTypes(practice_id=2,
                                    event_name='Test Event Type 12',
                                    event_description='Test Event Type 12 Description',
                                    event_status='Active')
    # Test practice persons
    test_person_1 = People(practice_id=2,
                           first_name='Test',
                           middle_name='Test',
                           last_name='Test',
                           suffix_name='Test',
                           address_1='123 Main St',
                           address_2='Suite 100',
                           city='San Francisco',
                           state='CA',
                           zipcode='94105',
                           phone_number='5555555555',
                           phone_type='Mobile',
                           email='test@soulstone.com',
                           status='Active',
                           gender_identity='She/Her')
    test_person_2 = People(practice_id=2,
                           first_name='Test2',
                           last_name='Test2',
                           phone_number='5555555555',
                           phone_type='Mobile',
                           status='Active')

    # Add to the database
    db.session.add(support_practice)
    db.session.add(test_practice)
    db.session.add(support_user)
    db.session.add(test_user)
    db.session.add(test_charge_1)
    db.session.add(test_charge_2)
    db.session.add(test_event_type_1)
    db.session.add(test_event_type_2)
    db.session.add(test_event_type_3)
    db.session.add(test_event_type_4)
    db.session.add(test_event_type_5)
    db.session.add(test_event_type_6)
    db.session.add(test_event_type_7)
    db.session.add(test_event_type_8)
    db.session.add(test_event_type_9)
    db.session.add(test_event_type_10)
    db.session.add(test_event_type_11)
    db.session.add(test_event_type_12)
    db.session.add(test_person_1)
    db.session.add(test_person_2)
    db.session.commit()
    print('Database seeded')

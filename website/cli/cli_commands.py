'''
CLI Commands for the website app
'''

# Imports
from flask import Blueprint
from werkzeug.security import generate_password_hash
from website.models import Practice, User, People, Charges
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

    # Add to the database
    db.session.add(support_practice)
    db.session.add(test_practice)
    db.session.add(support_user)
    db.session.add(test_user)
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
    db.session.add(test_person_1)
    db.session.add(test_person_2)
    db.session.commit()
    print('Database seeded')

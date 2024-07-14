"""Util to populate the DB with fake date"""
import random

from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash

from users.models import User
from app import db


faker = Faker()

# Blueprint configuration
faker_bp = Blueprint('commands', __name__)


@faker_bp.cli.command('seed_users')
def seed_users():
    """Seeds the database with fake user data"""

    user_data = []

    # Users
    for i in range(1, 100+1):
        user_data.append(User(
            practice_id=1,
            email=faker.email(),
            password=generate_password_hash('password'),
            first_name=faker.first_name(),
            last_name=faker.last_name()
        ))

    for entry in user_data:
        db.session.add(entry)
    db.session.commit()


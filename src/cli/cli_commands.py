"""
CLI Commands for the website app
"""

# Imports
import random
from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash
from src.models import (
    Practice,
    User,
    People,
    Charges,
    EventTypes,
    Notes,
)
from src import db

# Faker instance
fake = Faker()

# Blueprint Configuration
commands = Blueprint("commands", __name__)


# Flask CLI commands
@commands.cli.command("db_create")
def db_create():
    """Use "flask db_create" to create the database in the terminal"""
    db.create_all()
    print("Database created")


@commands.cli.command("db_drop")
def db_drop():
    """Use "flask db_drop" to drop the database in the terminal"""
    db.drop_all()
    print("Databased dropped")


@commands.cli.command("db_seed")
def db_seed():
    """Preloads the database with data"""
    # Data to seed the database with
    data = []

    # Support practice
    support_practice = Practice(
        name="Support Practice",
        email="support@email.com",
        website="www.support.com",
        phone_number="5555555555",
        phone_type="Office",
        address_1="123 Main St",
        address_2="Suite 100",
        city="San Francisco",
        state="CA",
        zipcode="94105",
        status="Active",
    )

    # Test practice
    test_practice = Practice(
        name="Test Practice",
        email="test@email.com",
        website="www.test.com",
        phone_number="5555555555",
        phone_type="Office",
        address_1="123 Main St",
        address_2="Suite 100",
        city="San Francisco",
        state="CA",
        zipcode="94105",
        status="Active",
    )

    # Support user
    support_user = User(
        practice_id=1,
        email="rodneygauna+support@gmail.com",
        password=generate_password_hash(
            "rodneygauna+support", method="sha256"),
        first_name="Support",
        last_name="User",
        role="Support",
        status="Active",
    )

    # Test user
    test_user = User(
        practice_id=2,
        email="rodneygauna+hh@gmail.com",
        password=generate_password_hash("rodneygauna+hh", method="sha256"),
        first_name="Rodney",
        last_name="Gauna",
        role="Practitioner",
        user_type="Owner",
        status="Active",
    )

    # Test practice charges
    for i in range(1, 11):
        data.append(
            Charges(
                practice_id=2,
                code=f"TestCharge{i}",
                name=f"Test Charge {i}",
                description=f"Test Charge {i} Description",
                amount=round(random.uniform(1.00, 1000.00)),
                status="Active",
            )
        )

    # Test Event Types
    for i in range(1, 11):
        data.append(
            EventTypes(
                practice_id=2,
                event_name=f"Test Event Type {i}",
                event_description=f"Test Event Type {i} Description",
                event_status="Active",
            )
        )

    # Test practice persons
    for i in range(1, 1100):
        data.append(
            People(
                practice_id=2,
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                suffix_name=fake.suffix(),
                address_1=fake.street_address(),
                address_2=fake.secondary_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                zipcode=fake.zipcode(),
                phone_number=fake.random_number(digits=10),
                phone_type=fake.random_element(
                    elements=("Mobile", "Office", "Home", "Fax")),
                email=fake.email(),
                status="Active",
                gender_identity="She/Her",
            )
        )

    # Test practice notes
    for i in range(1, 1100):
        data.append(
            Notes(
                practice_id=2,
                person_id=i,
                date_of_service=fake.date_between(
                    start_date="-1y", end_date="today"),
                reason_for_visit=fake.sentence(),
                visit_notes=fake.paragraph(),
                post_visit_recommendations=fake.paragraph(),
            )
        )

    # Add to the database
    db.session.add(support_practice)
    db.session.add(test_practice)
    db.session.add(support_user)
    db.session.add(test_user)

    for entry in data:
        db.session.add(entry)

    db.session.commit()
    print("Database seeded")

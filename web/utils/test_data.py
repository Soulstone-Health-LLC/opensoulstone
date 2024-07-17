"""
CLI Commands for the website app
"""

# Imports
import random
import time
from datetime import datetime, timezone, timedelta
from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash
from billing.models import Charges, LedgerCharges, LedgerPayments
from events.models import Events, EventTypes
from persons.models import People
from settings.models import Practice
from support.models import ReleaseNotes
from terms_of_service.models import TermsOfService
from users.models import User
from visit_notes.models import Notes
from dictionary.general import (
    STATE_CHOICES, GENDER_PRONOUN_CHOICES, PHONE_TYPE_CHOICES,
    ROLE_CHOICES, USER_TYPE_CHOICES, PAYMENT_TYPE_CHOICES,
    EVENT_DURATION_CHOICES, CHAKRA_SCORE_CHOICES,
    VISIT_NOTE_STATUS_CHOICES,
)
from app import db

# Faker instance
fake = Faker()

# Blueprint Configuration
commands = Blueprint("commands", __name__)


# CLI Commands - Database Seeding
# Seed Practice
@commands.cli.command("db_seed_practice")
def db_seed_practice():
    """Preloads the database with a practice"""

    time.sleep(10)

    practice_data = []

    for i in range(1, 11):
        practice_data.append(Practice(
            name=f"Test Practice {i}",
            email=fake.email(),
            website=fake.url(),
            phone_number=random.randint(1000000000, 9999999999),
            phone_type="Office",
            address_1=fake.street_address(),
            address_2=fake.building_number(),
            city=fake.city(),
            state=random.choice([item[0] for item in STATE_CHOICES]),
            zipcode=fake.postcode(),
            status=random.choice(['Active', 'Inactive']),
        ))

    for entry in practice_data:
        db.session.add(entry)
    db.session.commit()


# Seed Users
@commands.cli.command("db_seed_users")
def db_seed_users():
    """Preloads the database with users"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    user_data = []

    # For each practice, create 10 users
    for practice_id in practice_ids:
        for i in range(1, 11):
            user_data.append(User(
                practice_id=practice_id,
                email=fake.email(),
                password=generate_password_hash("password"),
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                suffix_name=fake.suffix(),
                address_1=fake.street_address(),
                address_2=fake.secondary_address(),
                city=fake.city(),
                state=random.choice([item[0] for item in STATE_CHOICES]),
                zipcode=fake.postcode(),
                phone_number=random.randint(1000000000, 9999999999),
                phone_type=random.choice([item[0]
                                         for item in PHONE_TYPE_CHOICES]),
                role=random.choice([item[0] for item in ROLE_CHOICES]),
                user_type=random.choice([item[0]
                                        for item in USER_TYPE_CHOICES]),
                status=random.choice(['Active', 'Inactive']),
            ))

    for entry in user_data:
        db.session.add(entry)
    db.session.commit()


# Seed People
@commands.cli.command("db_seed_people")
def db_seed_people():
    """Preloads the database with people"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    people_data = []

    # For each practice, create 500 people
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]

        for i in range(1, 501):
            people_data.append(People(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                suffix_name=fake.suffix(),
                address_1=fake.street_address(),
                address_2=fake.secondary_address(),
                city=fake.city(),
                state=random.choice([item[0] for item in STATE_CHOICES]),
                zipcode=fake.postcode(),
                phone_number=random.randint(1000000000, 9999999999),
                phone_type=random.choice([item[0]
                                         for item in PHONE_TYPE_CHOICES]),
                email=fake.email(),
                status=random.choice(['Active', 'Inactive']),
                date_of_birth=fake.date_between(
                    start_date="-1y", end_date="today"),
                gender_identity=random.choice(
                    [item[0] for item in GENDER_PRONOUN_CHOICES]),
            ))

    for entry in people_data:
        db.session.add(entry)
    db.session.commit()


# Seed Charges
@commands.cli.command("db_seed_charges")
def db_seed_charges():
    """Preloads the database with charges"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    charge_data = []

    # For each practice, create 100 charges and ensure that each charge
    # is associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]

        for i in range(1, 101):
            charge_data.append(Charges(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                code=f"TestCharge{i}",
                name=f"Test Charge {i}",
                description=f"Test Charge {i} Description",
                amount=round(random.uniform(1.00, 1000.00)),
                tax_rate=round(random.uniform(0.00, 0.50)),
                status=random.choice(['Active', 'Inactive']),
            ))

    for entry in charge_data:
        db.session.add(entry)
    db.session.commit()


# Seed Ledger Charges
@commands.cli.command("db_seed_ledger_charges")
def db_seed_ledger_charges():
    """Preloads the database with ledger charges"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    ledger_charge_data = []

    # For each practice, create 100 ledger charges and ensure that each
    # ledger charge is associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]
        person_ids = [person.id for person in People.query.filter_by(
            practice_id=practice_id).all()]
        charge_ids = [charge.id for charge in Charges.query.filter_by(
            practice_id=practice_id).all()]

        for i in range(1, 101):
            ledger_charge_data.append(LedgerCharges(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                created_at=fake.date_between(
                    start_date="-1y", end_date="today"),
                charge_id=random.choice(charge_ids),
                person_id=random.choice(person_ids),
                units=random.randint(1, 10),
                unit_amount=round(random.uniform(1.00, 1000.00)),
            ))

    for entry in ledger_charge_data:
        db.session.add(entry)
    db.session.commit()


# Seed Ledger Payments
@commands.cli.command("db_seed_ledger_payments")
def db_seed_ledger_payments():
    """Preloads the database with ledger payments"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    ledger_payment_data = []

    # For each practice, create 100 ledger payments and ensure that each
    # ledger payment is associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]
        person_ids = [person.id for person in People.query.filter_by(
            practice_id=practice_id).all()]

        for i in range(1, 101):
            ledger_payment_data.append(LedgerPayments(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                created_at=fake.date_between(
                    start_date="-1y", end_date="today"),
                person_id=random.choice(person_ids),
                amount=round(random.uniform(1.00, 1000.00)),
                payment_method=random.choice(
                    [item[0] for item in PAYMENT_TYPE_CHOICES]),
                payment_note=fake.paragraph(),
            ))

    for entry in ledger_payment_data:
        db.session.add(entry)
    db.session.commit()


# Seed Event Types
@commands.cli.command("db_seed_event_types")
def db_seed_event_types():
    """Preloads the database with event types"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    event_type_data = []

    # For each practice, create 10 event types and ensure that each event
    # type is associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]

        for i in range(1, 11):
            event_type_data.append(EventTypes(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                event_name=f"Test Event Type {i}",
                event_description=f"Test Event Type {i} Description",
                event_status=random.choice(['Active', 'Inactive']),
            ))

    for entry in event_type_data:
        db.session.add(entry)
    db.session.commit()


# Seed Events
@commands.cli.command("db_seed_events")
def db_seed_events():
    """Preloads the database with events"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    event_data = []

    # For each practice, create 100 events and ensure that each event is
    # associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]
        person_ids = [person.id for person in People.query.filter_by(
            practice_id=practice_id).all()]
        event_type_ids = [event_type.id for event_type in EventTypes.query.filter_by(
            practice_id=practice_id).all()]

        for i in range(1, 101):
            start_time = fake.time_object()

            # Select a random end time increment: 15, 30, 45, or 60 minutes
            end_time_increments = [15, 30, 45, 60]
            end_time_increment = random.choice(end_time_increments)

            # Calculate the end time
            end_time = (datetime.combine(datetime.min, start_time) +
                        timedelta(minutes=end_time_increment)).time()

            event_data.append(Events(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                event_type_id=random.choice(event_type_ids),
                person_id=random.choice(person_ids),
                date=fake.date_between(
                    start_date="-120d", end_date="today"),
                start_time=start_time,
                end_time=end_time,
                note=fake.paragraph(),
            ))

    for entry in event_data:
        db.session.add(entry)
    db.session.commit()


# Seed Visit Notes
@commands.cli.command("db_seed_visit_notes")
def db_seed_visit_notes():
    """Preloads the database with visit notes"""

    practice_ids = [practice.id for practice in Practice.query.all()]

    visit_notes_data = []

    # For each practice, create 1000 visit notes and ensure that each visit
    # note is associated with a user id of that practice
    for practice_id in practice_ids:

        user_of_practice = [
            user.id for user in User.query.filter_by(practice_id=practice_id).all()
        ]
        person_ids = [person.id for person in People.query.filter_by(
            practice_id=practice_id).all()]

        for i in range(1, 1001):

            random_date = fake.date_between(start_date="-1y", end_date="today")

            visit_notes_data.append(Notes(
                practice_id=practice_id,
                created_by=random.choice(user_of_practice),
                created_at=random_date,
                person_id=random.choice(person_ids),
                date_of_service=random_date,
                reason_for_visit=fake.sentence(),
                chakra_assessment_root_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_root_description=fake.paragraph(),
                chakra_assessment_sacral_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_sacral_description=fake.paragraph(),
                chakra_assessment_solar_plexus_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_solar_plexus_description=fake.paragraph(),
                chakra_assessment_heart_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_heart_description=fake.paragraph(),
                chakra_assessment_throat_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_throat_description=fake.paragraph(),
                chakra_assessment_third_eye_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_third_eye_description=fake.paragraph(),
                chakra_assessment_crown_score=random.choice(
                    [item[0] for item in CHAKRA_SCORE_CHOICES]),
                chakra_assessment_crown_description=fake.paragraph(),
                visit_notes=fake.paragraph(),
                post_visit_recommendations=fake.paragraph(),
                status=random.choice([item[0]
                                     for item in VISIT_NOTE_STATUS_CHOICES]),
            ))

    for entry in visit_notes_data:
        db.session.add(entry)
    db.session.commit()


# Seed Release Notes
@commands.cli.command("db_seed_release_notes")
def db_seed_release_notes():
    """Preloads the database with release notes"""

    release_notes_data = []

    for i in range(1, 11):
        random_date = fake.date_between(start_date="-1y", end_date="today")

        release_notes_data.append(ReleaseNotes(
            release_note_date=random_date,
            release_note_content=fake.paragraph(),
            created_at=random_date,
            created_by=1,
        ))

    for entry in release_notes_data:
        db.session.add(entry)
    db.session.commit()


# Seed Terms of Service
@commands.cli.command("db_seed_terms_of_service")
def db_seed_terms_of_service():
    """Preloads the database with terms of service"""

    terms_of_service = TermsOfService(
        created_date=datetime.now(timezone.utc),
        created_by=1,
        active_date=datetime.now(timezone.utc),
        sunset_date=datetime.now(timezone.utc) + timedelta(days=365),
        version=str(datetime.now(timezone.utc)),
        content="""
<h2>Terms of Service Agreement</h2>
<h3>User Responsibilities</h3>
<p>
1.1. Acceptable Use: User agrees to use the Application in a lawful and
responsible manner and to comply with all applicable laws and regulations.
</p>
<p>
1.2. Account Security: User is responsible for maintaining the security of
their account credentials and ensuring that unauthorized access does not
occur.
</p>
<p>
1.3. User Content: User acknowledges that they are solely responsible for
any content they upload, submit, or transmit through the Application and
that such content complies with applicable laws and regulations.
</p>
<h3>Intellectual Property</h3>
<p>
2.1. Ownership: The Application and all associated intellectual property
rights belong to the Company. User acknowledges that they do not acquire
any ownership rights by using the Application.
</p>
<p>
2.2. License: The Company grants User a limited, non-exclusive,
non-transferable license to use the Application for its intended purpose.
</p>
<h3>Privacy</h3>
<p>
3.1. Data Collection: User acknowledges and agrees that the Company may
collect and process certain personal data as outlined in the Privacy
Policy.
</p>
<p>
3.2. Cookies: The Application may use cookies or similar technologies to
enhance the User experience. By using the Application, User consents to
the use of cookies in accordance with our Cookie Policy.
</p>
<h3>Limitation of Liability</h3>
<p>
4.1. Disclaimer: The Application is provided on an "as is" and "as
available" basis, without warranties of any kind, either expressed or
implied. The Company disclaims all warranties, including but not limited
to, fitness for a particular purpose, non-infringement, and accuracy of
information.
</p>
<p>
4.2. Indemnification: User agrees to indemnify and hold the Company
harmless from any claims, damages, liabilities, and expenses arising out
of their use of the Application or violation of this Agreement.
</p>
<h3>Termination</h3>
<p>
5.1. Termination Rights: The Company reserves the right to suspend or
terminate User's access to the Application at any time, with or without
cause, and without prior notice.
</p>
<h3>Governing Law</h3>
<p>
6.1. Jurisdiction: This Agreement shall be governed by and construed in
accordance with the laws of the United States of America. Any disputes
arising from this Agreement shall be subject to the exclusive jurisdiction
of the courts in the United States of America.
</p>
<br />
<p>
Please read this Agreement carefully before using the Application. By
accessing or using the Application, you acknowledge that you have read,
understood, and agree to be bound by this Agreement.
</p>"""
    )

    db.session.add(terms_of_service)
    db.session.commit()

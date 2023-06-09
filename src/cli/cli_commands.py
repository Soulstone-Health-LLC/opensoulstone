"""
CLI Commands for the website app
"""

# Imports
import random
from datetime import datetime, timedelta
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
    TermsOfService,
    Events,
    LedgerCharges,
    LedgerPayments,
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

    # Terms of Service
    terms_of_service = TermsOfService(
        created_at=datetime.now(),
        created_by=1,
        active_date=datetime.now(),
        sunset_date=datetime.now() + timedelta(days=365),
        version=str(datetime.now()),
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
                person_id=random.randint(1, 1100),
                date_of_service=fake.date_between(
                    start_date="-1y", end_date="today"),
                reason_for_visit=fake.sentence(),
                chakra_assessment_root_score=random.randint(-5, 5),
                chakra_assessment_root_description=fake.paragraph(),
                chakra_assessment_sacral_score=random.randint(-5, 5),
                chakra_assessment_sacral_description=fake.paragraph(),
                chakra_assessment_solar_plexus_score=random.randint(-5, 5),
                chakra_assessment_solar_plexus_description=fake.paragraph(),
                chakra_assessment_heart_score=random.randint(-5, 5),
                chakra_assessment_heart_description=fake.paragraph(),
                chakra_assessment_throat_score=random.randint(-5, 5),
                chakra_assessment_throat_description=fake.paragraph(),
                chakra_assessment_third_eye_score=random.randint(-5, 5),
                chakra_assessment_third_eye_description=fake.paragraph(),
                chakra_assessment_crown_score=random.randint(-5, 5),
                chakra_assessment_crown_description=fake.paragraph(),
                visit_notes=fake.paragraph(),
                post_visit_recommendations=fake.paragraph(),
            )
        )

    # Test practice events
    for i in range(1, 1100):
        data.append(
            Events(
                practice_id=2,
                person_id=random.randint(1, 1100),
                event_type_id=random.randint(1, 11),
                practitioner_id=2,
                date=fake.date_between(
                    start_date="-1y", end_date="today"),
                start_time=fake.time_object(),
                end_time=fake.time_object(),
                note=fake.paragraph(),
            )
        )

    # Test practice ledger charges
    for i in range(1, 2100):
        data.append(
            LedgerCharges(
                practice_id=2,
                charge_id=random.randint(1, 11),
                person_id=random.randint(1, 1100),
                units=1,
                unit_amount=round(random.uniform(1.00, 1000.00)),
            )
        )

    # Test practice ledger payments
    for i in range(1, 1100):
        data.append(
            LedgerPayments(
                practice_id=2,
                person_id=random.randint(1, 2100),
                amount=round(random.uniform(1.00, 200.00)),
                payment_method=fake.random_element(
                    elements=("Cash", "Check", "Credit Card", "Other")),
                payment_note=fake.paragraph(),
            )
        )

    # Add to the database
    db.session.add(terms_of_service)
    db.session.add(support_practice)
    db.session.add(test_practice)
    db.session.add(support_user)
    db.session.add(test_user)

    for entry in data:
        db.session.add(entry)

    db.session.commit()
    print("Database seeded")

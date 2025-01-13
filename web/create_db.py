"""Create the database and the tables."""
import time
import os
from werkzeug.security import generate_password_hash
from app import app, db
from users.models import User
from settings.models import Practice

time.sleep(5)

SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL")
SUPPORT_PASSWORD = os.environ.get("SUPPORT_PASSWORD")


with app.app_context():
    db.create_all()

    # Check if "Support" practice is in the database
    support_practice = Practice.query.filter_by(
        name="Soulstone Support").first()

    # If not, create a new practice
    if support_practice is None:
        support_practice = Practice(
            name="Soulstone Support",
            address_1="123 Support St.",
            city="Supportville",
            state="Support",
            zipcode=12345,
            phone_number="1234567890",
            phone_type="Mobile",
        )
        db.session.add(support_practice)
        db.session.commit()

    # Check if "rodney@soulstonehealth.com" is a user in the database
    user = User.query.filter_by(email=SUPPORT_EMAIL).first()

    # If not, create a new user
    if user is None:
        user = User(
            email=SUPPORT_EMAIL,
            password=generate_password_hash(SUPPORT_PASSWORD),
            first_name="Rodney",
            last_name="Gauna",
            role="Support"
        )
        db.session.add(user)
        db.session.commit()

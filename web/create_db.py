"""Create the database and the tables."""
import time
import os
import sys
from werkzeug.security import generate_password_hash
from app import app, db
from users.models import User
from settings.models import Practice

# Wait for database to be ready (especially important in Docker)
time.sleep(5)

# Required environment variables
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL")
SUPPORT_PASSWORD = os.environ.get("SUPPORT_PASSWORD")

# Optional environment variables for practice configuration
PRACTICE_NAME = os.environ.get("PRACTICE_NAME", "Default Practice")
PRACTICE_ADDRESS = os.environ.get("PRACTICE_ADDRESS", "123 Main Street")
PRACTICE_CITY = os.environ.get("PRACTICE_CITY", "Your City")
PRACTICE_STATE = os.environ.get("PRACTICE_STATE", "Your State")
PRACTICE_ZIPCODE = os.environ.get("PRACTICE_ZIPCODE", "12345")
PRACTICE_PHONE = os.environ.get("PRACTICE_PHONE", "555-123-4567")
PRACTICE_PHONE_TYPE = os.environ.get("PRACTICE_PHONE_TYPE", "Office")


def validate_required_config():
    """Validate that required configuration is present."""
    missing_vars = []

    if not SUPPORT_EMAIL:
        missing_vars.append("SUPPORT_EMAIL")
    if not SUPPORT_PASSWORD:
        missing_vars.append("SUPPORT_PASSWORD")

    if missing_vars:
        print("ERROR: Missing required environment variables: "
              f"{', '.join(missing_vars)}")
        print("Please ensure your .env file is properly configured.")
        sys.exit(1)


def create_default_practice():
    """Create or update the default practice."""
    print("Checking for default practice...")

    # Look for any existing practice first
    existing_practice = Practice.query.first()

    if existing_practice is None:
        print(f"Creating default practice: {PRACTICE_NAME}")
        zipcode_int = (int(PRACTICE_ZIPCODE)
                       if PRACTICE_ZIPCODE.isdigit() else 12345)
        practice = Practice(
            name=PRACTICE_NAME,
            address_1=PRACTICE_ADDRESS,
            city=PRACTICE_CITY,
            state=PRACTICE_STATE,
            zipcode=zipcode_int,
            phone_number=PRACTICE_PHONE,
            phone_type=PRACTICE_PHONE_TYPE,
        )
        db.session.add(practice)
        db.session.commit()
        print("✓ Default practice created successfully")
    else:
        print(f"✓ Practice '{existing_practice.name}' already exists")


def create_support_user():
    """Create or update the support user."""
    print(f"Checking for support user: {SUPPORT_EMAIL}")

    # Check if support user exists
    user = User.query.filter_by(email=SUPPORT_EMAIL).first()

    if user is None:
        print("Creating support user...")
        user = User(
            email=SUPPORT_EMAIL,
            password=generate_password_hash(SUPPORT_PASSWORD),
            first_name="Support",
            last_name="Admin",
            role="Support"
        )
        db.session.add(user)
        db.session.commit()
        print("✓ Support user created successfully")
    else:
        print("✓ Support user already exists")


# Main initialization
if __name__ == "__main__":
    print("Starting database initialization...")

    try:
        # Validate configuration
        validate_required_config()

        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created")

            # Create default practice
            create_default_practice()

            # Create support user
            create_support_user()

            print("✓ Database initialization completed successfully!")

    except Exception as e:
        print(f"ERROR: Database initialization failed: {str(e)}")
        sys.exit(1)

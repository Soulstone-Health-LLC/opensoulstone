'''
Query the database for the charges select field
'''


# Imports
from flask_login import current_user
from website import db
from website.models import Charges


# SQL query for the people select field
charges_query = db.session.query(Charges.id, Charges.name).filter_by(practice_id=current_user.practice_id).order_by(
    Charges.name).all()

# Create a list of tuples for the people select field
possible_charges = {
    charge.id: f'{charge.name}' for charge in charges_query}

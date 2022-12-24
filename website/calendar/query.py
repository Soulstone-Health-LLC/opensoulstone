'''
Query the database for the people select field
'''


# Imports
from website import db
from website.models import People

# SQL query for the people select field
people_query = db.session.query(People.id, People.first_name, People.last_name).order_by(
    People.last_name).all()  # TODO: need to add practice_id filter

# Create a list of tuples for the people select field
possible_people = {
    person.id: f'{person.first_name} {person.last_name}'
    for person in people_query}

"""Create the database and the tables."""
import time
from app import app, db

time.sleep(5)


with app.app_context():
    db.create_all()

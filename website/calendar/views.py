'''
Views for the calendar section of the website
'''

# Imports
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.calendar.forms import AddEventForm
from website import db
from website.models import Events


# Blueprint
calendar = Blueprint('calendar', __name__)


# Routes
# Calendar Page
@calendar.route('/calendar')
@login_required
def schedule():
    '''Calendar page'''
    # TODO: Add sql query to get calendar data

    return render_template("calendar.html",
                           title="Calendar",
                           user=current_user)


# Add Event Page
@calendar.route('/calendar/add_event', methods=['GET', 'POST'])
@login_required
def addEvent():
    '''Add Event page'''
    form = AddEventForm()

    form.person.choices = [(person.id, person.first_name + ' ' + person.last_name)
                           for person in current_user.practice.people]

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_type = form.event_type.data
            person_id = form.person.data
            date = form.date.data
            time = form.time.data
            note = form.note.data

            # Create new event
            new_event = Events(practice_id=practice_id,
                               created_at=created_at,
                               created_by=created_by,
                               updated_at=updated_at,
                               updated_by=updated_by,
                               event_type=event_type,
                               person_id=person_id,
                               date=date,
                               time=time,
                               note=note)

            # Add new event to the database
            db.session.add(new_event)
            db.session.commit()

            # Flash message
            flash('New event created', 'success')

            # Redirect to the calendar page
            return redirect(url_for('calendar.schedule'))
    return render_template("add_event.html",
                           form=form,
                           user=current_user)

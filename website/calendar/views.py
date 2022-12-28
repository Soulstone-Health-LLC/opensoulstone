'''
Views for the calendar section of the website
'''

# Imports
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.calendar.forms import AddEventForm
from website import db
from website.models import Events, People, EventTypes


# Blueprint
calendar = Blueprint('calendar', __name__)


# Routes
# Calendar Page
@calendar.route('/calendar')
@login_required
def schedule():
    '''Calendar page'''
    if request.method == 'GET':
        events = db.session.query(Events.created_at,
                                  Events.start_date,
                                  Events.start_time,
                                  Events.end_date,
                                  Events.end_time,
                                  People.first_name,
                                  People.middle_name,
                                  People.last_name,
                                  People.suffix_name,
                                  EventTypes.event_name)\
            .join(People, Events.person_id == People.id)\
            .join(EventTypes, Events.event_type_id == EventTypes.id)\
            .filter_by(practice_id=current_user.practice_id).all()

        cal_events = [{
            'title': f'{event.first_name} {event.last_name} ({event.event_name})',
            'start': str(event.start_date) + 'T' + str(event.start_time),
            'end': str(event.end_date) + 'T' + str(event.end_time),
            'url': url_for('calendar.schedule')
        } for event in events]

    return render_template("calendar.html",
                           title="Calendar",
                           events=cal_events,  # TODO: Fix this
                           cal_events=events,  # TODO: Flip this
                           user=current_user)


# Add Event Page
@ calendar.route('/calendar/add_event', methods=['GET', 'POST'])
@ login_required
def addEvent():
    '''Add Event page'''
    form = AddEventForm()

    form.event_type_id.choices = [(event_type.id, event_type.event_name) for event_type
                                  in current_user.practice.event_types]

    form.person.choices = [(0, 'None')] + [(person.id, person.first_name + ' ' + person.last_name)
                                           for person in current_user.practice.people]

    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_type_id = form.event_type_id.data
            person_id = form.person.data
            start_date = form.start_date.data
            start_time = form.start_time.data
            end_date = form.end_date.data
            end_time = form.end_time.data
            note = form.note.data

            # Create new event
            new_event = Events(practice_id=practice_id,
                               created_at=created_at,
                               created_by=created_by,
                               updated_at=updated_at,
                               updated_by=updated_by,
                               event_type_id=event_type_id,
                               person_id=person_id,
                               start_date=start_date,
                               start_time=start_time,
                               end_date=end_date,
                               end_time=end_time,
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

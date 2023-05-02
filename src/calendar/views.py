'''
Views for the calendar section of the website
'''

# Imports
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.calendar.forms import EventForm
from src import db
from src.models import Events, People, EventTypes


# Blueprint
calendar = Blueprint('calendar', __name__)


# Routes
# Calendar Page
@calendar.route('/calendar')
@login_required
def schedule():
    '''Calendar page'''
    if request.method == 'GET':
        events = db.session.query(Events.id,
                                  Events.created_at,
                                  Events.date,
                                  Events.start_time,
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
            'start': str(event.date) + 'T' + str(event.start_time),
            'end': str(event.date) + 'T' + str(event.end_time),
            'url': url_for('calendar.viewEvent', event_id=event.id)
        } for event in events]

    return render_template("calendar/calendar.html",
                           title="Calendar",
                           events=cal_events,  # TODO: Fix this
                           cal_events=events,  # TODO: Flip this
                           user=current_user)


# Add Event Page
@ calendar.route('/calendar/add_event', methods=['GET', 'POST'])
@ login_required
def addEvent():
    '''Add Event page'''
    form = EventForm()

    form.event_type_id.choices = [(event_type.id, event_type.event_name) for event_type
                                  in current_user.practice.event_types]

    form.person.choices = [(0, 'None')] + [(person.id, person.first_name + ' ' + person.last_name)
                                           for person in current_user.practice.people]

    if form.validate_on_submit():
        if request.method == 'POST':
            # calculate duration
            duration = EventTypes.query.filter_by(
                id=form.event_type_id.data).first().event_duration
            start_datetime = datetime.combine(
                form.date.data, form.start_time.data)
            # Get data from the form
            practice_id = current_user.practice_id
            created_at = datetime.utcnow()
            created_by = current_user.get_id()
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_type_id = form.event_type_id.data
            person_id = form.person.data
            date = form.date.data
            note = form.note.data

            # Calculate end date and time
            end_time = start_datetime + duration

            # Create new event
            new_event = Events(practice_id=practice_id,
                               created_at=created_at,
                               created_by=created_by,
                               updated_at=updated_at,
                               updated_by=updated_by,
                               event_type_id=event_type_id,
                               person_id=person_id,
                               date=date,
                               start_time=datetime.time(start_datetime),
                               end_time=datetime.time(end_time),
                               note=note)

            # Add new event to the database
            db.session.add(new_event)
            db.session.commit()

            # Flash message
            flash('New event created', 'success')

            # Redirect to the calendar page
            return redirect(url_for('calendar.schedule'))
    return render_template("calendar/add_event.html",
                           form=form,
                           user=current_user)


# View Event
@calendar.route('/calendar/view_event/<int:event_id>')
@login_required
def viewEvent(event_id):
    '''View Event page'''
    event = db.session.query(Events.id,
                             Events.created_at,
                             Events.date,
                             Events.start_time,
                             Events.end_time,
                             People.first_name,
                             People.middle_name,
                             People.last_name,
                             People.suffix_name,
                             EventTypes.event_name)\
        .filter_by(id=event_id)\
        .join(People, Events.person_id == People.id)\
        .join(EventTypes, Events.event_type_id == EventTypes.id).first()

    return render_template("calendar/view_event.html",
                           event=event,
                           user=current_user)


# Edit Event
@calendar.route('/calendar/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def editEvent(event_id):
    '''Edit Event page'''
    event = Events.query.get_or_404(event_id)
    form = EventForm()

    form.event_type_id.choices = [(event_type.id, event_type.event_name) for event_type
                                  in current_user.practice.event_types]

    form.person.choices = [(0, 'None')] + [(person.id, person.first_name + ' ' + person.last_name)
                                           for person in current_user.practice.people]

    if form.validate_on_submit():
        if request.method == 'POST':
            # calculate duration
            duration = EventTypes.query.filter_by(
                id=form.event_type_id.data).first().event_duration
            start_datetime = datetime.combine(
                form.date.data, form.start_time.data)
            # Get data from the form
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_type_id = form.event_type_id.data
            person_id = form.person.data
            date = form.date.data
            note = form.note.data

            # Calculate end date and time
            end_time = start_datetime + duration

            # Update event
            event.updated_at = updated_at
            event.updated_by = updated_by
            event.event_type_id = event_type_id
            event.person_id = person_id
            event.date = date
            event.start_time = datetime.time(start_datetime)
            event.end_time = datetime.time(end_time)
            event.note = note

            # Add new event to the database
            db.session.commit()

            # Flash message
            flash('Event updated', 'success')

            # Redirect to the calendar page
            return redirect(url_for('calendar.schedule'))
    elif request.method == 'GET':
        form.event_type_id.data = event.event_type_id
        form.person.data = event.person_id
        form.date.data = event.date
        form.start_time.data = event.start_time
        form.note.data = event.note

    return render_template("calendar/edit_event.html",
                           form=form,
                           event=event,
                           user=current_user)


# Delete Event
@calendar.route('/calendar/delete_event/<int:event_id>', methods=['POST'])
@login_required
def deleteEvent(event_id):
    '''Delete Event page'''
    event = Events.query.filter_by(id=event_id).first()

    # Delete event
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()

        # Flash message
        flash('Event deleted', 'success')

        # Redirect to the calendar page
        return redirect(url_for('calendar.schedule'))

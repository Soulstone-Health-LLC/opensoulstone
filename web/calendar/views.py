"""
Calendar > Views - This file contains the views for the Calendar Blueprint.
"""

# Imports
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from calendar.forms import EventForm
from app import db
from users.models import User
from calendar.models import Events, EventTypes
from persons.models import People


# Blueprint
calendar = Blueprint("calendar", __name__)


# Calendar Page
@calendar.route("/calendar")
@login_required
def schedule():
    """Calendar page"""

    start_date = datetime.now() - timedelta(days=120)

    if request.method == "GET":
        events = (
            db.session.query(
                Events.id,
                Events.created_at,
                Events.date,
                Events.start_time,
                Events.end_time,
                People.first_name,
                People.middle_name,
                People.last_name,
                People.suffix_name,
                EventTypes.event_name,
            )
            .outerjoin(People, Events.person_id == People.id)
            .join(EventTypes, Events.event_type_id == EventTypes.id)
            .filter(Events.practice_id == current_user.practice_id,
                    Events.date >= start_date)
            .all()
        )

        cal_events = [
            {
                "title": "Blocked Off Time"
                if event.first_name is None
                else f"""
                    {event.first_name} {event.last_name} ({event.event_name})
                """,
                "start": str(event.date) + "T" + str(event.start_time),
                "end": str(event.date) + "T" + str(event.end_time),
                "url": url_for("calendar.viewEvent", event_id=event.id),
            }
            for event in events
        ]

    return render_template(
        "calendar/calendar.html",
        title="Calendar",
        events=cal_events,
        cal_events=events,
        user=current_user,
    )


# Add Event Page
@calendar.route("/calendar/add_event", methods=["GET", "POST"])
@login_required
def addEvent():
    """Add Event page"""
    form = EventForm()

    # Choices of Event Types
    event_types = (
        db.session.query(EventTypes)
        .filter_by(practice_id=current_user.practice_id)
        .order_by(EventTypes.event_name)
    )

    form.event_type_id.choices = [
        (
            event_type.id,
            f"{event_type.event_name} "
            f"({event_type.event_duration.seconds // 3600} hours, "
            f"{event_type.event_duration.seconds // 60 % 60} minutes)",
        )
        for event_type in event_types
    ]

    # Choices of People
    persons = (
        db.session.query(People)
        .filter_by(practice_id=current_user.practice_id)
        .order_by(People.last_name)
    )

    form.person.choices = [(0, "None")] + [
        (
            person.id,
            person.last_name
            + ", "
            + person.first_name
            + f" ({person.gender_identity})",
        )
        for person in persons
    ]

    # Choices of Users that have a role of Practitioner
    practictioners = (
        db.session.query(User)
        .filter_by(practice_id=current_user.practice_id, role="Practitioner")
        .order_by(User.first_name)
    )

    form.practitioner_id.choices = [(0, "None")] + [
        (practictioner.id,
         practictioner.first_name + " " + practictioner.last_name)
        for practictioner in practictioners
    ]

    if form.validate_on_submit():
        if request.method == "POST":
            # calculate duration
            duration = (
                EventTypes.query.filter_by(id=form.event_type_id.data)
                .first()
                .event_duration
            )
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
            practitioner_id = form.practitioner_id.data
            date = form.date.data
            note = form.note.data

            # Calculate end date and time
            end_time = start_datetime + duration

            # Create new event
            new_event = Events(
                practice_id=practice_id,
                created_at=created_at,
                created_by=created_by,
                updated_at=updated_at,
                updated_by=updated_by,
                event_type_id=event_type_id,
                person_id=person_id,
                practitioner_id=practitioner_id,
                date=date,
                start_time=datetime.time(start_datetime),
                end_time=datetime.time(end_time),
                note=note,
            )

            # Add new event to the database
            db.session.add(new_event)
            db.session.commit()

            # Flash message
            flash("New event created", "success")

            # Redirect to the calendar page
            return redirect(url_for("calendar.schedule"))
    return render_template("calendar/add_event.html", form=form,
                           user=current_user)


# View Event
@calendar.route("/calendar/view_event/<int:event_id>")
@login_required
def viewEvent(event_id):
    """View Event page"""
    event = (
        db.session.query(
            Events.id,
            Events.created_at,
            Events.date,
            Events.start_time,
            Events.end_time,
            People.id.label("person_id"),
            People.first_name.label("person_first_name"),
            People.middle_name,
            People.last_name.label("person_last_name"),
            People.suffix_name,
            People.gender_identity,
            EventTypes.event_name,
            User.id.label("practitioner_id"),
            User.first_name.label("practitioner_first_name"),
            User.last_name.label("practitioner_last_name"),
        )
        .filter_by(id=event_id)
        .outerjoin(People, Events.person_id == People.id)
        .join(EventTypes, Events.event_type_id == EventTypes.id)
        .outerjoin(User, Events.practitioner_id == User.id)
        .first()
    )

    return render_template("calendar/view_event.html", event=event,
                           user=current_user)


# Edit Event
@calendar.route("/calendar/edit_event/<int:event_id>", methods=["GET", "POST"])
@login_required
def editEvent(event_id):
    """Edit Event page"""
    event = Events.query.get_or_404(event_id)
    form = EventForm()

    # Choices of Event Types
    event_types = (
        db.session.query(EventTypes)
        .filter_by(practice_id=current_user.practice_id)
        .order_by(EventTypes.event_name)
    )

    form.event_type_id.choices = [
        (
            event_type.id,
            f"{event_type.event_name} "
            f"({event_type.event_duration.seconds // 3600} hours, "
            f"{event_type.event_duration.seconds // 60 % 60} minutes)",
        )
        for event_type in event_types
    ]

    # Choices of People
    persons = (
        db.session.query(People)
        .filter_by(practice_id=current_user.practice_id)
        .order_by(People.last_name)
    )

    form.person.choices = [(0, "None")] + [
        (
            person.id,
            person.first_name + " " + person.last_name +
            f" ({person.gender_identity})",
        )
        for person in persons
    ]

    # Choices of Users that have a role of Practitioner
    practictioners = (
        db.session.query(User)
        .filter_by(practice_id=current_user.practice_id, role="Practitioner")
        .order_by(User.first_name)
    )

    form.practitioner_id.choices = [(0, "None")] + [
        (practictioner.id,
         practictioner.first_name + " " + practictioner.last_name)
        for practictioner in practictioners
    ]

    if form.validate_on_submit():
        if request.method == "POST":
            # calculate duration
            duration = (
                EventTypes.query.filter_by(id=form.event_type_id.data)
                .first()
                .event_duration
            )
            start_datetime = datetime.combine(
                form.date.data, form.start_time.data)
            # Get data from the form
            updated_at = datetime.utcnow()
            updated_by = current_user.get_id()
            event_type_id = form.event_type_id.data
            practitioner_id = form.practitioner_id.data
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
            event.practitioner_id = practitioner_id
            event.date = date
            event.start_time = datetime.time(start_datetime)
            event.end_time = datetime.time(end_time)
            event.note = note

            # Add new event to the database
            db.session.commit()

            # Flash message
            flash("Event updated", "success")

            # Redirect to the calendar page
            return redirect(url_for("calendar.schedule"))
    elif request.method == "GET":
        form.event_type_id.data = event.event_type_id
        form.person.data = event.person_id
        form.practitioner_id.data = event.practitioner_id
        form.date.data = event.date
        form.start_time.data = event.start_time
        form.note.data = event.note

    return render_template(
        "calendar/edit_event.html", form=form, event=event, user=current_user
    )


# Delete Event
@calendar.route("/calendar/delete_event/<int:event_id>", methods=["POST"])
@login_required
def deleteEvent(event_id):
    """Delete Event page"""
    event = Events.query.filter_by(id=event_id).first()

    # Delete event
    if request.method == "POST":
        db.session.delete(event)
        db.session.commit()

        # Flash message
        flash("Event deleted", "success")

        # Redirect to the calendar page
        return redirect(url_for("calendar.schedule"))

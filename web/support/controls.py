"""Support > Controllers - controls for the support blueprint"""
# Imports
from flask_mail import Message
from app import mail


# Send email
def send_email(subject, recipient, body):
    """Sends an email to the recipient with the specified subject and body."""

    msg = Message(subject, recipients=[
                  recipient], sender="donotreply@openvolunteer.com")
    msg.body = body
    mail.send(msg)

'''
    File name: models.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, secret_key


# ------------------------------------------------------------------------------
# Models
# Database Schema: https://drawsql.app/webdevable-llc/diagrams/soulstone
# ------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    '''SQL Table: user'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'),
                            default=1)
    practice = db.relationship('Practice')
    # Data Points - Create/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Data Points - Main
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150), nullable=False)
    suffix_name = db.Column(db.String(150))
    address_1 = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String(10))
    role = db.Column(db.String(50), nullable=False, default='Staff')
    status = db.Column(db.Text, nullable=False, default='Active')

    # For Reset/Forgot Password
    def get_token(self, expires_sec=900):
        serial = Serializer(secret_key, expires_in=expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(secret_key)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'{self.email} : {self.date_created}'


class Practice(db.Model):
    '''SQL Table: practice'''
    __tablename__ = 'practice'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    timezone_id = db.Column(db.Integer, db.ForeignKey('timezone.id'))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True))
    # Data Points - Main
    name = db.Column(db.Text, nullable=False)
    biography = db.Column(db.Text)
    address_1 = db.Column(db.Text, nullable=False)
    address_2 = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    phone_type = db.Column(db.String(10), nullable=False)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    status = db.Column(db.Text, nullable=False, default='Active')
    users = db.relationship('User')
    people = db.relationship('People')


class Timezone(db.Model):
    '''SQL Table: timezones'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    time_offset = db.Column(db.Integer)
    practices = db.relationship('Practice')


class People(db.Model):
    '''SQL Table: people'''
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    suffix_name = db.Column(db.String(150))
    address_1 = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String(10))
    email = db.Column(db.Text)
    status = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender_identity = db.Column(db.Text)
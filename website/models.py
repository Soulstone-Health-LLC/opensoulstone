'''
    File name: models.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import timezone
from . import db, secret_key
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.sql import func
import website
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# ------------------------------------------------------------------------------
# Models
# Database Schema: https://drawsql.app/webdevable-llc/diagrams/soulstone
# ------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    '''SQL Table: user'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    email = db.Column(db.Text)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    suffix_name = db.Column(db.String(150))
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String(10))
    role = db.Column(db.String(50))
    status = db.Column(db.Text)
    
    
    def get_token(self,expires_sec=900):
        serial = Serializer(secret_key, expires_in=expires_sec)
        return serial.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(secret_key)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    
class Practice(db.Model):
    '''SQL Table: practice'''
    __tablename__ = 'practice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    biography = db.Column(db.Text)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String(10))
    timezone_id = db.Column(db.Integer, db.ForeignKey('timezone.id'))
    users = db.relationship('User')
    

class Locations(db.Model):
    '''SQL Table: locations'''
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    address_1 = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    timezone_id = db.Column(db.Integer, db.ForeignKey('timezone.id'))
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String(10))
    email = db.Column(db.Text)
    status = db.Column(db.Boolean)
    
    
class Timezone(db.Model):
    '''SQL Table: timezones'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    time_offset = db.Column(db.Integer)
    practices = db.relationship('Practice')
    locations = db.relationship('Locations')
    

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
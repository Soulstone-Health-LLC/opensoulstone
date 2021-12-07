'''
    File name: models.py
    Author: Rodney Gauna
    Date created: 2021-10-31
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
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
    # Relationships
    users = db.relationship('User')
    people = db.relationship('People')


class People(db.Model):
    '''SQL Table: people'''
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Data Points - Main
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
    status = db.Column(db.Text, default='Active')
    date_of_birth = db.Column(db.Date)
    gender_identity = db.Column(db.Text)


class Charges(db.Model):
    '''SQL Table: charges'''
    __tablename__ = 'charges'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Data Points - Main
    code = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Text, default='Active')


class Notes(db.Model):
    ''' SQL Table: notes '''
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Data Points - Main
    date_of_service = db.Column(db.DateTime, nullable=False)
    reason_for_visit = db.Column(db.Text)
    chakra_assessment_root_score = db.Column(db.Integer)
    chakra_assessment_root_description = db.Column(db.Text)
    chakra_assessment_sacral_score = db.Column(db.Integer)
    chakra_assessment_sacral_description = db.Column(db.Text)
    chakra_assessment_solar_plexus_score = db.Column(db.Integer)
    chakra_assessment_solar_plexus_description = db.Column(db.Text)
    chakra_assessment_heart_score = db.Column(db.Integer)
    chakra_assessment_heart_description = db.Column(db.Text)
    chakra_assessment_throat_score = db.Column(db.Integer)
    chakra_assessment_throat_description = db.Column(db.Text)
    chakra_assessment_third_eye_score = db.Column(db.Integer)
    chakra_assessment_third_eye_description = db.Column(db.Text)
    chakra_assessmentcrown_score = db.Column(db.Integer)
    chakra_assessmentcrown_description = db.Column(db.Text)
    visit_notes = db.Column(db.Text)
    # Signed Status
    status = db.Column(db.Text, nullable=False, default='Open')

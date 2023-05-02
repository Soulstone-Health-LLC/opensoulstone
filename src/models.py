'''
Modles for the Soulstone application
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import timedelta
from flask import redirect, url_for
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager, SECRET_KEY


# ------------------------------------------------------------------------------
# LoginManager - user_loader
# ------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    '''Queries the database for the user_id and returns the user object'''
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    '''Redirects unauthorized users to the login page'''
    return redirect(url_for('users.login'))


# ------------------------------------------------------------------------------
# Model - Form Dictinaries
# ------------------------------------------------------------------------------
# State Dictionary
STATE_CHOICES = [('', ''), ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'),
                 ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'),
                 ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'),
                 ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
                 ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'),
                 ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'),
                 ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'),
                 ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
                 ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'),
                 ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'),
                 ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'),
                 ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'),
                 ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')]

# Gender Pronoun Dictionary
GENDER_PRONOUN_CHOICES = [('', ''),
                          ('He/Him', 'He/Him'),
                          ('She/Her', 'She/Her'),
                          ('They/Them', 'They/Them'),
                          ('He/Them', 'He/Them'),
                          ('She/Them', 'She/Them'),
                          ('Name/Name', 'Name/Name'),
                          ('Other', 'Other')]

# Phone Type Dictionary
PHONE_TYPE_CHOICES = [('Mobile', 'Mobile'),
                      ('Home', 'Home'),
                      ('Office', 'Office'),
                      ('Fax', 'Fax')]

# Role Dictionary
ROLE_CHOICES = [('Practitioner', 'Practitioner'),
                ('Staff', 'Staff')]

# Status Dictionary
STATUS_CHOICES = [('Active', 'Active'),
                  ('Inactive', 'Inactive')]

# Payment Type Dictionary
PAYMENT_TYPE_CHOICES = [('Cash', 'Cash'),
                        ('Check', 'Check'),
                        ('Credit Card', 'Credit Card'),
                        ('Gift Card', 'Gift Card'),
                        ('Other', 'Other')]


# ------------------------------------------------------------------------------
# Models - Database Tables
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
    phone_number = db.Column(db.String(10))
    phone_type = db.Column(db.String(10))
    role = db.Column(db.String(50), nullable=False, default='Staff')
    status = db.Column(db.Text, nullable=False, default='Active')

    # For Reset/Forgot Password
    def get_token(self, expires_sec=900):
        serial = Serializer(SECRET_KEY, expires_in=expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(SECRET_KEY)
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
    phone_number = db.Column(db.String(10), nullable=False)
    phone_type = db.Column(db.String(10), nullable=False)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    status = db.Column(db.Text, nullable=False, default='Active')
    # Relationships
    users = db.relationship('User')
    people = db.relationship('People')
    event_types = db.relationship('EventTypes')


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
    phone_number = db.Column(db.String(10))
    phone_type = db.Column(db.String(10))
    email = db.Column(db.Text)
    status = db.Column(db.Text, default='Active')
    date_of_birth = db.Column(db.Date)
    gender_identity = db.Column(db.Text)
    # Relationships
    events = db.relationship('Events')

    # Outstanding Balances
    def outstanding_balance(self):
        ''' Returns the sum of the person's ledger charges minus payments'''
        charge_sum = db.session.query(db.func.sum(LedgerCharges.unit_amount)).filter(
            LedgerCharges.person_id == self.id
        ).scalar()
        payment_sum = db.session.query(db.func.sum(LedgerPayments.amount)).filter(
            LedgerPayments.person_id == self.id
        ).scalar()

        return charge_sum - payment_sum


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


class LedgerCharges(db.Model):
    '''SQL Table: ledger_charges'''
    __tablename__ = 'ledger_charges'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    charge_id = db.Column(db.Integer, db.ForeignKey('charges.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Data Points - Main
    units = db.Column(db.Integer, nullable=False, default=1)
    unit_amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=0.0)
    # Relationships
    person = db.relationship(
        'People', backref=db.backref('ledger_charges', lazy=True))


class LedgerPayments(db.Model):
    '''SQL Table: ledger_payments'''
    __tablename__ = 'ledger_payments'
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
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)
    check_number = db.Column(db.String(50))
    credit_card_last_four = db.Column(db.Integer)
    payment_note = db.Column(db.Text)


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
    chakra_assessment_crown_score = db.Column(db.Integer)
    chakra_assessment_crown_description = db.Column(db.Text)
    visit_notes = db.Column(db.Text)
    post_visit_recommendations = db.Column(db.Text)
    # Signed Status
    status = db.Column(db.Text, nullable=False, default='Open')


class Events(db.Model):
    '''SQL Table: events'''
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    note = db.Column(db.Text)
    # Relationships
    event_type = db.relationship('EventTypes', backref='events', lazy=True)

    def __repr__(self):
        return f"Event('{self.event_type}', '{self.date}', '{self.time}')"


class EventTypes(db.Model):
    '''SQL Table: event_types'''
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_name = db.Column(db.Text, nullable=False)
    event_description = db.Column(db.Text)
    event_status = db.Column(db.Text, nullable=False, default='Active')
    event_duration = db.Column(
        db.Interval, nullable=False, default=timedelta(minutes=30))

    def __repr__(self):
        return f"Event_Type('{self.event_name}', '{self.event_description}')"

"""People/person models"""
# Import
from datetime import datetime, timezone
from billing.models import LedgerCharges, LedgerPayments
from app import db


class People(db.Model):
    """SQL Table: people"""

    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"))
    # Data Points - Created/Updated
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_at = db.Column(db.DateTime(timezone=True))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Data Points - Main
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    suffix_name = db.Column(db.String(150))
    address_1 = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.String(10))
    phone_number = db.Column(db.String(10))
    phone_type = db.Column(db.String(10))
    email = db.Column(db.Text)
    status = db.Column(db.Text, default="Active")
    date_of_birth = db.Column(db.Date)
    gender_identity = db.Column(db.Text)
    profile_image = db.Column(
        db.Text, nullable=False, default='default_profile.jpg')

    # Outstanding Balances
    def outstanding_balance(self):
        """Returns the outstanding balance for the person"""
        charge_sum = (
            db.session.query(
                db.func.coalesce(
                    db.func.sum(
                        db.func.ifnull(
                            LedgerCharges.unit_amount * LedgerCharges.units
                            + (LedgerCharges.unit_amount *
                               LedgerCharges.tax_rate),
                            0
                        )
                    ),
                    0
                )
            )
            .filter(
                LedgerCharges.person_id == self.id
            )
            .scalar()
        )
        payment_sum = (
            db.session.query(db.func.coalesce(
                db.func.sum(LedgerPayments.amount), 0))
            .filter(LedgerPayments.person_id == self.id)
            .scalar()
        )

        return (
            charge_sum - payment_sum
            if charge_sum is not None and payment_sum is not None
            else 0
        )

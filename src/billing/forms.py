"""
Billing > Froms - This file contains the forms for the billing blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, IntegerField, SelectField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired
from src.dictionary.general import PAYMENT_TYPE_CHOICES


# Form - Add Ledger Charge
class AddLedgerChargeForm(FlaskForm):
    """Add new Ledger Charge"""

    charge_id = SelectField(label="Charge *", coerce=int,
                            validators=[InputRequired()],
                            render_kw={
                                "class": "form-control select2 form-select"},
                            )
    unit_amount = FloatField(label="Unit Amount *")
    units = IntegerField(
        label="Units *", default=1, validators=[DataRequired(), Length(min=1)])
    tax_rate = FloatField(label="Tax Rate (Percentage)",
                          validators=[Length(min=1)])
    submit = SubmitField(label="Add Charge")


class AddLedgerPaymentForm(FlaskForm):
    """Add new Ledger Payment"""

    payment_amount = FloatField(
        label="Payment Amount *", validators=[DataRequired()])
    payment_method = SelectField(
        label="Payment Method *",
        choices=PAYMENT_TYPE_CHOICES,
        validators=[DataRequired()],
    )
    check_number = IntegerField(label="Check Number")
    credit_card_number = IntegerField(
        label="Credit Card Number", validators=[Length(min=4, max=4)]
    )
    payment_note = TextAreaField(label="Payment Note")
    submit = SubmitField(label="Add Payment")

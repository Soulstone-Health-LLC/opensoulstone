# soulstone/website/billing/forms.py
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length


# ------------------------------------------------------------------------------
# Form - Add Ledger Charge
# ------------------------------------------------------------------------------
class AddLedgerChargeForm(FlaskForm):
    ''' Add new Ledger Charge '''
    charge_id = IntegerField(label='Charge ID *', validators=[DataRequired()])
    unit_amount = FloatField(label='Unit Amount *', validators=[DataRequired()])
    units = IntegerField(label='Units *', validators=[DataRequired(),
                                                      Length(min=1)])
    tax_rate = FloatField(label='Tax Rate', validators=[Length(min=1)])
    submit = SubmitField(label='Add Charge')

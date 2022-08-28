# soulstone/website/billing/forms.py
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# ------------------------------------------------------------------------------
# Form - Add Ledger Charge
# ------------------------------------------------------------------------------
class AddLedgerChargeForm(FlaskForm):
    ''' Add new Ledger Charge '''
    units = StringField(label='Units *',
                        validators=[DataRequired(),
                                    Length(min=1)])
    tax_rate = StringField(label='Tax Rate',
                           validators=[Length(min=1)])
    submit = SubmitField(label='Add Charge')

# soulstone/website/billing/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website import db
from website.models import Practice, People, Notes, Charges
from website.models import LedgerCharges, LedgerPayments


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
billing = Blueprint('billing', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Billing
# ------------------------------------------------------------------------------
# Billing
@billing.route('/billing')
@login_required
def ledger():
    ''' Routes the user to the Billing page'''
    ledger_charges = db.session.query(LedgerCharges.created_at,
                                      LedgerCharges.units,
                                      LedgerCharges.unit_amount,
                                      LedgerCharges.practice_id,
                                      People.first_name,
                                      People.middle_name,
                                      People.last_name,
                                      People.suffix_name,
                                      Charges.code,
                                      Charges.description)\
        .join(People, LedgerCharges.person_id == People.id)\
        .join(Charges, LedgerCharges.charge_id == Charges.id)\
        .filter_by(practice_id=current_user.practice_id).all()

    return render_template("billing.html",
                           title="Soulstone - Billing",
                           user=current_user,
                           ledger_charges=ledger_charges)


# Payments
@billing.route('/billing/payments')
@login_required
def payments():
    ''' Routes the user to the Billing > Payments page'''
    ledger_payments = db.session.query(LedgerPayments.created_at,
                                       LedgerPayments.payment_method,
                                       LedgerPayments.amount,
                                       LedgerPayments.payment_note,
                                       LedgerPayments.practice_id,
                                       People.first_name,
                                       People.middle_name,
                                       People.last_name,
                                       People.suffix_name)\
        .join(People, LedgerPayments.person_id == People.id)\
        .filter_by(practice_id=current_user.practice_id).all()

    return render_template("payments.html",
                           title="Soulstone - Payments",
                           user=current_user,
                           ledger_payments=ledger_payments)

# soulstone/website/billing/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.billing.forms import AddLedgerChargeForm
from website import db
from website.models import People, Charges
from website.models import LedgerCharges, LedgerPayments, Notes


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
    people = People.query.filter_by(practice_id=current_user.practice_id).all()
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
                           people=people,
                           ledger_charges=ledger_charges)


# Billing - Add Ledger Charge
@billing.route('/billing/<int:id>/add_ledger_charge', methods=['GET', 'POST'])
@login_required
def addLedgerCharge(id):
    ''' Routes the user to the add new ledger charge page '''
    form = AddLedgerChargeForm()

    pers_id = People.query.get_or_404(id).id
    practice_charges = Charges.query.filter_by(
        practice_id=current_user.practice_id).all()

    # current user practice id
    pu_id = current_user.practice_id
    pp_id = People.query.get_or_404(id).practice_id
    notes_count = Notes.query.filter_by(person_id=id).count()

    if request.method == 'GET':
        # check if user practice id matches patient user id
        if pu_id == pp_id:
            # Display the person info
            person = People.query.get_or_404(id)
            #c_id = Charges.query.get_or_404(id).id

            return render_template("add_ledger_charge.html",
                                   title="Soulstone - Add New Charge",
                                   user=current_user,
                                   person=person,
                                   notes_count=notes_count,
                                   practice_charges=practice_charges,
                                   form=form)
        else:
            return render_template("401.html",
                                   user=current_user)

    if form.validate_on_submit and request.method == 'POST':
        practice_id = current_user.practice_id
        # charge_id =
        person_id = pers_id
        # note_id =
        created_at = datetime.utcnow()
        created_by = current_user.get_id()
        updated_at = datetime.utcnow()
        updated_by = current_user.get_id()
        units = form.units.data
        # unit_amount =
        tax_rate = form.tax_rate.data

        # Add new ledger charge to the database
        new_ledger_charge = LedgerCharges(practice_id=practice_id,
                                          # charge_id=charge_id,
                                          person_id=person_id,
                                          # note_id=note_id,
                                          created_at=created_at,
                                          created_by=created_by,
                                          updated_at=updated_at,
                                          updated_by=updated_by,
                                          units=units,
                                          # unit_amount=unit_amount,
                                          tax_rate=tax_rate)
        db.session.add(new_ledger_charge)
        db.session.commit()
        flash('Charge added successfully.',
              category='success')

        return redirect(url_for('settings.ledger'))

    return render_template("add_ledger_charge.html",
                           title="Soulstone - Add Charge",
                           user=current_user,
                           form=form)


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

# soulstone/website/billing/views.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template
from flask_login import login_required, current_user


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
    return render_template("billing.html", title="Soulstone - Billing",
                           user=current_user)

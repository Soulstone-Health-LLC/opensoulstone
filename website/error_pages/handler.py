# soulstone/website/error_pages/handler.py

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from flask import Blueprint, render_template


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
error_pages = Blueprint('error_pages', __name__)


# ------------------------------------------------------------------------------
# Routes - Practice - Error Pages
# ------------------------------------------------------------------------------
# 404 Page
@error_pages.errorhandler(401)
def page_401(e):
    ''' Displays 401 page if there is an error '''
    return render_template("401.html", title='Soulstone'), 401


# 404 Page
@error_pages.errorhandler(404)
def page_404(e):
    ''' Displays 404 page if there is an error '''
    return render_template("404.html", title='Soulstone')
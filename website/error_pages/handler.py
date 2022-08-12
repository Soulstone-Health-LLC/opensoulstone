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
# 401 Page
@error_pages.errorhandler(401)
def page_401(error):
    ''' Displays 401 page if there is an error '''
    return render_template("401.html", title='Soulstone'), 401


# 403 Page
@error_pages.errorhandler(403)
def page_403(error):
    ''' Displays 403 page if there is an error '''
    return render_template("403.html", title='Soulstone'), 403


# 404 Page
@error_pages.errorhandler(404)
def page_404(error):
    ''' Displays 404 page if there is an error '''
    return render_template("404.html", title='Soulstone')
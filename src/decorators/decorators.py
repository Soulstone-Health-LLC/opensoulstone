"""
Decorators for the application.
"""

# Imports
from functools import wraps
from flask import render_template
from flask_login import current_user


# Decorator to check if user is a Super User or Owner (Admin)
def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type not in [
            "Super User",
            "Owner",
        ]:
            return render_template("error_pages/403.html",
                                   title="Soulstone - 403 Unauthorized")
        return f(*args, **kwargs)

    return decorated_function

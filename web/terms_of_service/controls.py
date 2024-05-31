"""Terms of Service > Controls - Controllers for Terms of Service"""
# Imports
from sqlalchemy.orm import aliased
from users.models import User
from app import db
from .models import TermsOfService


# Terms of Service - Get Terms of Service Details
def get_tos_details(tos_id):
    """Get Terms of Service Details"""

    # Create aliases for the User table
    created_by_user = aliased(User)
    updated_by_user = aliased(User)

    # Get terms of service
    tos = (
        db.session.query(
            TermsOfService.id,
            TermsOfService.version,
            TermsOfService.content,
            TermsOfService.created_date,
            TermsOfService.created_by,
            TermsOfService.updated_date,
            TermsOfService.updated_by,
            TermsOfService.active_date,
            TermsOfService.sunset_date,
            created_by_user.first_name.label("created_by_first_name"),
            created_by_user.last_name.label("created_by_last_name"),
            updated_by_user.first_name.label("updated_by_first_name"),
            updated_by_user.last_name.label("updated_by_last_name"),
        )
        .join(created_by_user, TermsOfService.created_by == created_by_user.id)
        .outerjoin(updated_by_user,
                   TermsOfService.updated_by == updated_by_user.id)
        .filter(TermsOfService.id == tos_id)
        .first()
    )

    return tos

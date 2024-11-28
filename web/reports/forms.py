"""
Reports > Forms - This file contains the forms for the Reports Blueprint.
"""

# Imports
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired

# Form - Generate Report


class GenerateReportForm(FlaskForm):
    """Form to generate a report with start and end dates"""

    start_date = datetime.now() - timedelta(days=30)

    start_date = DateField(
        label="Start Date *",
        format="%Y-%m-%d",
        default=start_date,
        render_kw={"class": "form-control"},
        validators=[DataRequired()]
    )
    end_date = DateField(
        label="End Date *",
        format="%Y-%m-%d",
        default=datetime.now(),
        render_kw={"class": "form-control"},
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Generate Report")

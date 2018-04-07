"""Template for all forms on the website."""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField


class Create_post(FlaskForm):
    """Add planning to database."""

    title = StringField('Title',
                        validators=[DataRequired()]
                        )
    content = StringField('Content',
                          validators=[DataRequired()]
                          )

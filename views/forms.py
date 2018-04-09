"""Template for all forms on the website."""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField, FileField


class Create_post(FlaskForm):
    """Add planning to database."""

    title = StringField('Title',
                        validators=[DataRequired()]
                        )
    content = StringField('Content',
                          validators=[DataRequired()]
                          )


class Create_category(FlaskForm):
    """Category form."""

    name = StringField('Category name',
                       validators=[DataRequired()]
                       )
    image = FileField('image',
                          validators=[DataRequired()]
                          )

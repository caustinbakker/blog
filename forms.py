"""Template for all forms on the website."""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField, FileField, TextAreaField


class Category(FlaskForm):
    """Category form."""

    name = StringField('Category name', validators=[DataRequired()])
    image = FileField('image', validators=[DataRequired()])


class Post(FlaskForm):
    """Add planning to database."""

    name = StringField('Title', validators=[DataRequired()])
    file = FileField()
    file1 = FileField()
    content = TextAreaField('Content', validators=[DataRequired()])


class Project(FlaskForm):
    """Add Project to database."""

    name = StringField('Project Name', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])


class Login(FlaskForm):
    """Login form."""

    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Access code', validators=[DataRequired()])

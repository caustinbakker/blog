"""models."""
from peewee import *
import datetime


db = SqliteDatabase('database/blog.db')


class Project(Model):
    """Projects."""

    name = CharField(unique=True)

    class Meta(object):
        """Select database."""

        database = db


class Category(Model):
    """model for all avaible category's."""

    name = CharField(unique=True)
    image = CharField()

    class Meta(object):
        """Select database."""

        database = db


class Post(Model):
    """Model for posts."""

    name = CharField()
    content = CharField()
    imagepath = CharField(default='Null')
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db


def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Post, Project], safe=True)
    db.close()

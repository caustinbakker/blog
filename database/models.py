"""models."""
from peewee import *
import datetime


db = SqliteDatabase('database/blog.db')


class Category(Model):
    """model for all avaible category's."""

    name = CharField(unique=True)
    imagepath = CharField()

    class Meta(object):
        """Select database."""

        database = db


class Post(Model):
    """Model for posts."""

    title = CharField()
    content = CharField()
    imagepath = CharField(default='Null')
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db


def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Post], safe=True)
    db.close()

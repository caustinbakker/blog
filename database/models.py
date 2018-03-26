"""models."""
from peewee import *

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
    imagepath = CharField()

    class Meta(object):
        """Select database."""

        database = db


def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Post], safe=True)
    testfunctions()
    db.close()


def testfunctions():
    """Test function."""
    try:
        Category.create(
            name='CAD',
            imagepath='category/cad.jpg'
        )
        Category.create(
            name='Solidworks',
            imagepath='category/cad.jpg'
        )
    except IntegrityError:
        pass

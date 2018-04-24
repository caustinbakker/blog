"""models."""
from peewee import *
import datetime


db = SqliteDatabase('partials/blog.db')


class Project(Model):
    """Projects."""

    name = CharField(unique=True)

    class Meta(object):
        """Select database."""

        database = db

    def get_posts(self):
        """Grab all the posts from project."""
        return (ProjectPost.select().where(ProjectPost.project == self)
                .order_by(ProjectPost.created_date))


class Category(Model):
    """model for all avaible category's."""

    name = CharField(unique=True)
    image = CharField()

    class Meta(object):
        """Select database."""

        database = db


class ProjectPost(Model):
    """Model for posts."""

    project = ForeignKeyField(Project, backref='ProjectPost')
    name = CharField()
    content = CharField()
    image = CharField(default='Null')
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db


class Post(Model):
    """Model for posts."""

    name = CharField()
    content = CharField()
    image = CharField(default='Null')
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db


def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Post, Project, ProjectPost], safe=True)
    db.close()

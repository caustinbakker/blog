"""models."""
from app import db
from peewee import *
import datetime
from flask_login import UserMixin


class Project(Model):
    """Projects."""

    name = CharField(unique=True)
    content = CharField()
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db

    def get_project_media(self):
        """Grab image from get_posts."""
        post = Post.select().where(Post.project_id == self).get()
        return Media.select().where(Media.post_id == post).get().media

    def check_media(self):
        """Check if project has media."""
        try:
            post = Post.select().where(Post.project_id == self).get()
            Media.select().where(Media.post_id == post.id).get()
            print('True')
            return True
        except DoesNotExist:
            print('False')
            return False

    def with_media(self):
        """Grab image from get_posts."""
        media = Post.select(Post, Media).join(Media).where(Post.project_id ==
                                                           self)

        return bool(media)

    def media_url(self):
        """Return all posts that are accosicated with this project."""
        post = (Post.select()
                .where(Post.project_id == self).get())
        try:
            media = (Media.select()
                     .where(Media.post_id == post.id)
                     .get())
            return (media.media)
        except DoesNotExist:
            return False

    def posts(self):
        """Return all posts that are accosicated with this project."""
        return Post.select().where(Post.project_id == self)


class Post(Model):
    """Model for posts."""

    project = ForeignKeyField(Project, backref='Post', null=True, default=None)
    name = CharField()
    content = TextField()
    "Media Model"
    "Category Model"
    "Project Model"
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db

    def get_category(self):
        """Grab all the posts from project."""
        return (Category.select()
                .where(Category.post_id == self))

    def get_media(self):
        """Grab all media from this post."""
        return (Media.select()
                .where(Media.post_id == self))

    def standalone():
        """Return a model of all posts not bound to a project."""
        return (Post.select()
                .where(Post.project.is_null())
                .order_by(Post.created_date.desc()))

    def date():
        """Return dates order_by."""
        return(Post.select()
               .order_by(Post.created_date.desc()))


class Media(Model):
    """Media for post."""

    post = ForeignKeyField(Post, backref='Media')
    media = CharField()

    class Meta(object):
        """Select database."""

        database = db


class Category(Model):
    """model for all avaible category's."""

    post = ForeignKeyField(Post, backref='Category')
    name = CharField()

    class Meta(object):
        """Select database."""

        database = db

    def get_name():
        """Get all category's without overlaping."""
        categorys = Category.select()
        categoryList = []
        for category in categorys:
            categoryName = category.name.title()
            if categoryName not in categoryList:
                categoryList.append(categoryName)
        return categoryList


class User(UserMixin, Model):
    """User model for login."""

    email = CharField(unique=True, null=False)

    class Meta(object):
        """Database."""

        database = db



def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Project, Post, Media, User], safe=True)
    db.close()

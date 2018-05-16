"""models."""
from peewee import *
import datetime


db = MySQLDatabase('database',
                   host='35.233.225.232',
                   user='root',
                   passwd='qfIbhehmDHy9Ny6C')

class Project(Model):
    """Projects."""

    name = CharField(unique=True)
    content = CharField()
    created_date = DateTimeField(default=datetime.datetime.today())

    class Meta(object):
        """Select database."""

        database = db

    def get_posts(self):
        """Grab all the posts from project."""
        return (ProjectPost.select().where(ProjectPost.project == self)
                .order_by(ProjectPost.created_date))

    def image(self):
        """Grab image from get_posts."""
        try:
            return (ProjectPost.select().where(ProjectPost.project == self)
                    .order_by(ProjectPost.created_date).get().image)
        except Exception:
            pass

    def get_project_media(self):
        """Grab image from get_posts."""
        post = Post.select().where(Post.project_id == self).get()
        return Media.select().where(Media.post_id == post).get().media


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


def initialize():
    """Create tables."""
    db.connect()
    db.create_tables([Category, Project, Post, Media], safe=True)
    db.close()

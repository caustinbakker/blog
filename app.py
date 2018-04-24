"""Main script for the blog website."""
from flask import Flask
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
DEBUG = app.debug


import views


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    print(__file__)
    app.run()

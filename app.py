"""Main script for the blog website."""
from flask import Flask
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads

import models

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
DEBUG = app.debug


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from views import *


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    app.run()

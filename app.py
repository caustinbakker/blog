"""Main script for the blog website."""
from flask import Flask
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import LoginManager, login_user
from jinja2 import Environment

import models

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
DEBUG = app.debug

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from views import *


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    app.run()

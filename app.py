"""Main script for the blog's website."""
from flask import Flask, current_app
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import LoginManager, login_user
from flask_caching import Cache
from jinja2 import Environment
import logging
import os
import pymysql

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
DEBUG = app.debug

db = MySQLDatabase(database=app.config['CLOUDSQL_DATABASE'],
                   user=app.config['CLOUDSQL_USER'],
                   password=app.config['CLOUDSQL_PASSWORD'],
                   host='35.234.157.177')
db.connect()
db.close()
logging.info('Remote Connection to database')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def _get_storage_client():
    return storage.Client(
        project=app.config['PROJECT_ID'])


login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


import models
from views import *


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    DEBUG = True
    app.run()

"""Main script for the blog's website."""
from flask import Flask, current_app
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import LoginManager, login_user
from jinja2 import Environment
import os
import pymysql


try:
    db = MySQLDatabase(host='127.0.0.1', user='root', password='test', unix_socket='/cloudsql/austinbakkerblog:europe-west2:mydatabase1', database='database')
    db.connect()
    db.close()
except OperationalError:
    db = MySQLDatabase(host='35.234.157.177', database='database', user='austin', password='austin')
    db.connect()
    db.close()
    print('Connected via remote ip')


def _get_storage_client():
    print('app.config')
    print(app.config['PROJECT_ID'])
    return storage.Client(
        project=app.config['PROJECT_ID'])


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
DEBUG = app.debug


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import models
from views import *


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    app.run()

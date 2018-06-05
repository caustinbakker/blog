"""Main script for the blog's website."""
from flask import Flask, current_app
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import LoginManager, login_user
from jinja2 import Environment
import logging
import os
import pymysql

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
DEBUG = app.debug

try:
    db = MySQLDatabase(host='127.0.0.1',
                       user=app.config['CLOUDSQL_USER'],
                       password=app.config['CLOUDSQL_PASSWORD'],
                       unix_socket=app.config['CLOUDSQL_CONNECTION_NAME'],
                       database=app.config['CLOUDSQL_DATABASE'])
    db.connect()
    db.close()
    logging.info('Local connection to database')
except Exception:
    db = MySQLDatabase(host=app.config['CLOUDSQL_IP'],
                       database=app.config['CLOUDSQL_DATABASE'],
                       user=app.config['CLOUDSQL_USER'],
                       password=app.config['CLOUDSQL_PASSWORD'])
    db.connect()
    db.close()
    logging.info('Remote Connection to database')


def _get_storage_client():
    return storage.Client(
        project=app.config['PROJECT_ID'])


login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
    return oauth



import models
from views import *


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    app.run()

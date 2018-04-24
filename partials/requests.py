"""import app function."""
from app import app, DEBUG
from flask import g
from models import db
from peewee import OperationalError
import sass


@app.before_request
def before_request():
    """Connect database connect."""
    g.db = db
    css_complier(DEBUG)
    try:
        g.db.connect()
    except OperationalError:
        g.db.close()
        g.db.connect()


@app.after_request
def after_request(response):
    """Close database connection."""
    g.db.close()
    return response


def css_complier(debug):
    """Update Css if debug is true."""
    if debug is True:
        sass.compile(dirname=('static/styles/sass',
                              'static/styles/css'),
                     output_style='compressed')
        print('CSS updated')

"""import app function."""
from app import app, DEBUG, db
from flask import g
from peewee import OperationalError
import sass


@app.before_request
def before_request():
    """Connect database connect."""
    g.db = db
    try:
        g.db.connect()
    except OperationalError:
        g.db.close()
        g.db.connect()
    css_complier(DEBUG) # if debug is false then does not run sass compiler


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

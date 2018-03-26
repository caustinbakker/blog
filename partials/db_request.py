"""import app function."""
from __main__ import app
from database.models import db
from flask import g
from peewee import OperationalError


@app.before_request
def before_request():
    """Connect database connect."""
    g.db = db
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

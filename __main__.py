"""Main script for the blog website."""
from flask import Flask
from peewee import *

app = Flask(__name__, template_folder='views/templates',
            static_folder='views/static')
app.secret_key = '1243165fg78h2415634f35fdf89hg489hjf9092j23jjf9928fisd021j90j'


from partials import db_request

from database import models
from views import views


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
app.run(debug=True, port=5000, host='127.0.0.1')

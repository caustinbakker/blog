"""Main script for the blog website."""
from flask import Flask
from peewee import *
from flask_fileupload import FlaskFileUpload
from livereload import Server, shell

app = Flask(__name__,
            template_folder='views/templates',
            static_folder='views/static')
app.secret_key = '1243165fg78h2415634f35fdf89hg489hjf9092j23jjf9928fisd021j90j'
app.config['TEMPLATES_AUTO_RELOAD'] = True

ffu = FlaskFileUpload(app)


from partials import db_request

from database import models
from views import views

server = Server(app.wsgi_app)
# server.watch
server.serve()

if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    print(__file__)
app.run(debug=True, port=5500, host='127.0.0.1')

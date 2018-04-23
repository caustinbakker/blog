"""Main script for the blog website."""
from flask import Flask
from peewee import *
from livereload import Server, shell
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__, template_folder='views/templates')
app.secret_key = '1243165fg78h2415634f35fdf89hg489hjf9092j23jjf9928fisd021j90j'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
app.config['TEMPLATES_AUTO_RELOAD'] = True
configure_uploads(app, photos)


from partials import db_request

from database import models
from views import views


if __name__ == '__main__':
    models.initialize()
    print('=' * 100)
    print(__file__)
    # server = Server(app.wsgi_app)
    # server.watch('static/styles/*')
    # server.serve()
# app.run(debug=True, port=5500, host='127.0.0.1')

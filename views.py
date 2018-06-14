"""Main section for all views."""
from app import app, login_manager, _get_storage_client, cache
from flask import Flask, render_template, url_for, redirect, flash, request, session, jsonify, send_from_directory
from peewee import *
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime
# from flask_caching import Cached
from google.cloud import storage
import logging
import os
from urllib.parse import unquote
from flask_login import login_required, current_user, login_user
from flask_oauthlib.client import OAuth
oauth = OAuth(app)

import filters
import forms
import models

google = oauth.remote_app(
    'google',
    consumer_key=app.config['GOOGLE_CLIENT_ID'],
    consumer_secret=app.config['GOOGLE_CLIENT_SECRET'],
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))



@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user = google.get('userinfo').data
    email = user.get('email')
    userm = models.User.select().where(models.User.email == email).get()
    login_user(userm)
    return redirect('admin')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@login_manager.user_loader
def load_user(userid):
    return models.User(userid)

logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def main():
    """Display main webpage."""
    return render_template('main.html',
                           categorys=models.Category,
                           projects=models.Project,
                           posts=models.Post
                           )


@app.route('/blog', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def blog():
    """Display main webpage."""
    return render_template('blog.html',
                           posts=models.Post,
                           categorys=models.Category
                           )


@app.route('/about')
@cache.cached(timeout=50)
def about():
    """Render about_me.html."""
    return render_template('about_me.html')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """Display admin panel."""
    return render_template('admin.html',
                           posts=models.Post,
                           projects=models.Project)


@app.route('/admin/create/post/<int:id>', methods=['GET', 'POST'])
@login_required
def create_post(id=None):
    """Display form for creating a post."""
    form = forms.Post()
    if form.validate_on_submit():
        models.Post.create(project_id=id,
                           name=form.name.data,
                           content=form.content.data)
        post = (models.Post.select()
                .where(
                    (models.Post.name == form.name.data),
                    (models.Post.content == form.content.data)).get())
        for fileid in request.files:
            logging.debug('detected file id by {}'.format(fileid))
            file = request.files.get(str(fileid))
            logging.debug('fileid = {}'.format(fileid))
            upload_file(file, post.id)
        return redirect(url_for('admin'))
    return render_template('create_post.html', form=form)


@app.route('/admin/delete/<int:id>/<model>/<name>')
@login_required
def delete_item(model, id, name):
    """Delete a item."""
    models.db.execute_sql("DELETE FROM {} WHERE id = {}".format(model, id))
    flash(u'You deleted {} from {}'.format(name, model), 'Success')
    return redirect(url_for('admin'))


@app.route('/project/<id>')
def project(id=None):
    """Display Project."""
    if id is '0':
        return render_template('all_projects.html',
                               projects=models.Project.select())
    return render_template('project.html',
                           project=models.Project.get(models.Project.id == id)
                           )

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

def upload_file(file, post_id):
    """Save file."""
    path = 'post/{}/'.format(post_id)
    path = path.lower()
    filepath = (path + str(file.filename)).lower()
    file.save()
    logging.debug('uploaded {} at {}'.format(file.name, url))
    save_media_url(post_id, url)

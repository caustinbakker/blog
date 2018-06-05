"""Main section for all views."""
from app import app, login_manager, _get_storage_client
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import *
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime
from google.cloud import storage
import logging
import os
from urllib.parse import unquote

import filters
import forms
import models


logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def main():
    """Display main webpage."""
    return render_template('main.html',
                           categorys=models.Category,
                           projects=models.Project,
                           posts=models.Post
                           )


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    """Display main webpage."""
    return render_template('blog.html',
                           posts=models.Post,
                           categorys=models.Category
                           )


@app.route('/about')
def about():
    """Render about_me.html."""
    return render_template('about_me.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Display admin panel."""
    return render_template('admin.html',
                           posts=models.Post,
                           projects=models.Project)


@app.route('/admin/create/post/<int:id>', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login screen."""
    form = forms.Login()
    if form.validate_on_submit():
        if (password == form.password.data):
            flash('Login Sucessfull')
            return redirect(url_for('admin'))
        else:
            flash('Login failed!')
    return render_template('login.html', form=form)


def save_media_url(post_id, url):
    """Save url to post id."""
    logging.debug('Saving {} URL to {} post id'.format(url, post_id))
    models.Media.create(
        post_id=post_id,
        media=url)


def upload_file(file, post_id):
    """Save file."""
    path = 'post/{}/'.format(post_id)
    path = path.lower()
    filepath = (path + str(file.filename)).lower()
    try:
        client = _get_storage_client()
    except Exception:
        client = storage.Client.from_service_account_json(
            'service_account.json')
    bucket = client.bucket(app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filepath)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type)
    url = blob.public_url
    url = unquote(url)
    logging.debug('uploaded {} at {}'.format(file.name, url))
    save_media_url(post_id, url)

"""Main section for all views."""
from app import app, login_manager, _get_storage_client
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import *
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime
import os
from google.cloud import storage

import filters
import forms
import models


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


@app.route('/admin/create/<int:id>', methods=['GET', 'POST'])
def create_p(id):
    """Create a new item in the database."""
    form = forms.Project()
    if form.validate_on_submit():
        models.Post.create(project_id=id,
                           name=form.name.data,
                           content=form.content.data)
        post = (models.Post.select()
                .where(
                    (models.Post.name == form.name.data),
                    (models.Post.content == form.content.data)).get())

        filenames = request.files('')
        for filename in filenames:
            try:
                upload_image_file(request.files.get(filename), post.id)
            except AttributeError:
                pass
        return redirect(url_for('admin'))
    try:
        project = (models.Project.select()
                   .where(models.Project.id == id).get())
        return render_template('create_p.html', form=form,
                               project=project)
    except DoesNotExist:
        flash('No project by that id', 'fail')
        return 'Ha, no project'


@app.route('/admin/create/post', methods=['GET', 'POST'])
def create_post():
    """Display form for creating a post."""
    form = forms.Post()
    if form.validate_on_submit():
        models.Post.create(name=form.name.data,
                           content=form.content.data)
        post = (models.Post.select()
                .where(
                    (models.Post.name == form.name.data),
                    (models.Post.content == form.content.data)).get())
        print(post)
        for filename in request.files:
            upload_image_file(request.files.get(filename), int(post.id))
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


def upload_image_file(file, post_id):
    """Save file."""
    try:
        print('running upload image file')
        path = 'post/' + '{}/'.format(post_id)
        path = path.lower()
        filepath = (path + str(file.filename)).lower()
        try:
            file.save(filepath)
        except FileNotFoundError:
            os.makedirs(path)
            file.save(filepath)
        client = _get_storage_client()
        bucket = client.bucket(app.config['CLOUD_STORAGE_BUCKET'])
        blob = bucket.blob(filepath)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type)
        url = blob.public_url
        print(url)
        print(post_id)
        models.Media.create(
            post_id=post_id,
            media=url)
    except Exception:
        return 'error'


def jpg_converter():
    """Convert png files to jpg for optimisation."""
    pass


# def save_file(file, model, form, project_id):
#     """Save file."""
#     if project_id is not None:
#         path = (str('static/' + str(model._meta.table_name)) +
#                 '/' + str(project_id) + '/')
#     else:
#         path = str('static/' + str(model._meta.table_name) + '/')
#     try:
#         filename = form.name.data + '.' + file.filename.split('.')[-1]
#     except Exception:
#         pass
#
#     filepath = str(path + filename).lower()
#     print(filepath)
#     try:
#         file.save(filepath)
#     except FileNotFoundError:
#         print('Creating File for images | ' + str(path))
#         os.makedirs(path)
#         file.save(filepath)
#     except Exception:
#         print('error')
#     return '/' + filepath

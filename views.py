"""Main section for all views."""
from app import app, login_manager
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import *
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime
import os

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

@app.route('/admin/create', methods=['GET', 'POST'])
@app.route('/admin/create/<int:id>', methods=['GET', 'POST'])
def create_p(id=None):
    """Create a new item in the database."""
    # if project_id is not None:
    #     model = str(model.title() + 'Post')
    #     form = getattr(forms, model)
    #     model = getattr(models, model)
    #     items.update({'project_id': project_id})
    # else:
    #     form = getattr(forms, model.title())
    #     model = getattr(models, model.title())
    form = forms.Post()
    if form.validate_on_submit():
        # try:
        #     file = request.files['image']
        #     filepath = save_file(file, model, form, project_id)
        #     print('returned filepath' + ' ' + filepath)
        #     items.update({'image': filepath})
        # except Exception:
        #     pass

        # for field in form:
        #     if field.id != 'image':
        #         items.update({field.id: field.data})
        models.Post.create(project_id=id,
                           name=form.name.data,
                           content=form.content.data)
        return redirect(url_for('admin'))
    return render_template('create_item.html', form=form)


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


def save_file(file, model, form, project_id):
    """Save file."""
    if project_id is not None:
        path = (str('static/' + str(model._meta.table_name)) +
                '/' + str(project_id) + '/')
    else:
        path = str('static/' + str(model._meta.table_name) + '/')
    try:
        filename = form.name.data + '.' + file.filename.split('.')[-1]
    except Exception:
        pass

    filepath = str(path + filename).lower()
    print(filepath)
    try:
        file.save(filepath)
    except FileNotFoundError:
        print('Creating File for images | ' + str(path))
        os.makedirs(path)
        file.save(filepath)
    except Exception:
        print('error')
    return '/' + filepath

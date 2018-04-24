"""Main section for all views."""
from app import app
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import DoesNotExist
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os

import forms
import models


@app.route('/', methods=('GET', 'POST'))
def main():
    """Display main webpage."""
    return render_template('main.html',
                           categorys=models.Category,
                           projects=models.Project)


@app.route('/<category>')
def category(category=None):
    """Display posts from category."""
    try:
        categorys = models.Category.get(models.Category.name == category)

    except DoesNotExist:
        return redirect(url_for('main'))
    return render_template('category.html', category=categorys)


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    """Display admin panel."""
    flash('Hello world!', 'success')
    return render_template('admin_panel.html',
                           categorys=models.Category,
                           posts=models.Post,
                           projects=models.Project)


@app.route('/admin/create/<model>', methods=['GET', 'POST'])
@app.route('/admin/create/<model>/<project_id>', methods=['GET', 'POST'])
def create_item(model, project_id=None):
    """Create a new item in the database."""
    items = {}
    if project_id is not None:
        model = str(model.title() + 'Post')
        form = getattr(forms, model)
        model = getattr(models, model)
        items.update({'project_id': project_id})
    else:
        form = getattr(forms, model.title())
        model = getattr(models, model.title())
    form = form()
    if form.validate_on_submit():
        try:
            file = request.files['image']
            filepath = save_file(file, model, form, project_id)
            print('returned filepath' + ' ' + filepath)
            items.update({'image': filepath})
        except Exception:
            pass

        for field in form:
            if field.id != 'image':
                items.update({field.id: field.data})
        model.create(**items)
        return redirect(url_for('admin_panel'))
    return render_template('create_item.html', form=form)


@app.route('/admin/delete/<int:id>/<model>/<name>')
def delete_item(model, id, name):
    """Delete a item."""
    models.db.execute_sql("DELETE FROM {} WHERE id = {}".format(model, id))
    flash(u'You deleted {} from {}'.format(name, model), 'Success')
    return redirect(url_for('admin_panel'))


@app.route('/project/<id>')
def project(id):
    """Display Project."""
    return render_template('project.html',
                           project=models.Project.get(models.Project.id == id)
                           )

from partials.requests import *


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

    filepath = str(path + filename)
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
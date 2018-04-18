"""Main section for all views."""
from __main__ import app
from database import models
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import DoesNotExist
from views import forms
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
configure_uploads(app, photos)


@app.route('/', methods=('GET', 'POST'))
def main():
    """Display main webpage."""
    # flash('You were successfully logged in')
    # flash('You were successfully logged in')
    return render_template('main.html',
                           categorys=models.Category,
                           posts=models.Post.select())


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
def create_item(model):
    """Create a new item in the database."""
    form = getattr(forms, model.title())
    form = form()
    if form.validate_on_submit():
        items = {}
        model = getattr(models, model.title())
        file = request.files['image']
        filename = form.name.data + '.' +file.filename.split('.')[-1]
        try:
            file.save('static/' + str(model._meta.table_name) + '/' +
                      filename)
        except FileNotFoundError:
            os.mkdir('static/' + str(model._meta.table_name))
            file.save('static/' + str(model._meta.table_name) + '/' +
                      filename)

        items.update({'image': str(model._meta.table_name) + '/' + str(filename)})
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


@app.route('/projects/<id>')
def project(id):
    """Display Project."""
    # display's project in timeline form

"""Main section for all views."""
from __main__ import app
from database import models
from flask import Flask, render_template, url_for, redirect, flash, request
from peewee import DoesNotExist
from views import forms
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
import os
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
configure_uploads(app, photos)


@app.route('/', methods=('GET', 'POST'))
def main():
    """Display main webpage."""
    # flash('You were successfully logged in')
    # flash('You were successfully logged in')
    return render_template('main.html', categorys=models.Category, posts=models.Post.select().order_by(models.Post.created_date.desc()))


@app.route('/<category>')
def category(category=None):
    """Display posts from category."""
    try:
        categorys = models.Category.get(models.Category.name == category)

    except DoesNotExist:
        return redirect(url_for('main'))
    return render_template('category.html', category=categorys)


# admin
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    """Display admin panel."""
    return render_template('admin_panel.html', categorys=models.Category.select(),
                           posts=models.Post.select())


@app.route('/admin/create_post', methods=['GET', 'POST'])
def create_post():
    """Create a blog post."""
    form = forms.Create_post()
    if form.validate_on_submit():
        models.Post.create(
            title=form.title.data,
            content=form.content.data
        )
        return 'Success'
    return render_template('create_post.html', form=form)


@app.route('/admin/create_category', methods=['GET', 'POST'])
def create_category():
    """Create a category."""
    form = forms.Create_category()
    if form.validate_on_submit():
        photos.save(request.files['image'])
        flash('Category added, sucess')
    return render_template('create_category.html', form=form)

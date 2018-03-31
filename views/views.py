"""Main section for all views."""
from __main__ import app
from database import models
from flask import Flask, render_template

from views import forms


@app.route('/', methods=('GET', 'POST'))
def main():
    """Display main webpage."""
    return render_template('main.html', categorys=models.Category)


@app.route('/<category>')
def category(category):
    """Display posts from category."""
    return render_template('category.html', category=models.Category.
                           get(models.Category.name == category))


@app.route('/create_post')
def create_post():
    """Create a blog post."""
    form = forms.Create_post()
    return render_template('create_post.html', form=form)

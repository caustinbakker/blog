"""Main section for all views."""
from __main__ import app
from database import models
from flask import Flask, render_template, url_for, redirect, flash
from peewee import DoesNotExist
from views import forms


@app.route('/', methods=('GET', 'POST'))
def main():
    """Display main webpage."""
    flash('You were successfully logged in')
    flash('You were successfully logged in')
    return render_template('main.html', categorys=models.Category)


@app.route('/<category>')
def category(category=None):
    """Display posts from category."""
    try:
        categorymodel = models.Category.get(models.Category.name == category)
    except DoesNotExist:
        return redirect(url_for('main'))
    return render_template('category.html', category=categorymodel)


@app.route('/create_post')
def create_post():
    """Create a blog post."""
    form = forms.Create_post()
    return render_template('create_post.html', form=form)

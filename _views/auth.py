"""Auth validation for server."""
from app import app, login_manager
import forms
import models
from flask_login import (login_required, current_user, login_user, logout_user)
from flask import render_template, redirect, url_for


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user."""
    form = forms.Login()
    if form.validate_on_submit():
        try:
            user = models.User.select().where(form.email.data == models.User.email).get()
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('admin'))
            else:
                raise Exception('Email or Password is wrong')
        except Exception:
            return ('Email or Password is wrong')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out user."""
    logout_user()
    return redirect(url_for('main'))

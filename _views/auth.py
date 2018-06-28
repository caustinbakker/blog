"""Auth validation for server."""
from app import app, login_manager
import forms
import models
from flask_login import (login_required, current_user, login_user, logout_user)
from flask import render_template, redirect, url_for, session, jsonify, request
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key='10522ca4f8794b6ce6ca',
    consumer_secret='ace0f28f53e97662966db9cd282e9f8a70eb054f',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)
oauth.init_app(app)


@app.route('/login/github')
def login_github():
    """Login via github."""
    return github.authorize(callback=url_for('authorized_github', _external=True))


@app.route('/login/github/authorized')
def authorized_github():
    """Authorize github account and add token."""
    resp = github.authorized_response()
    print('user: {} | access token: {}'.format(resp.get('email'),
                                               resp.get('access_token')))
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    email = github.get('user').data.get('email')
    user = models.User.select().where(email == models.User.email).get()
    login_user(user)
    return redirect(url_for('admin'))


@github.tokengetter
def get_github_oauth_token():
    """Grab token from github."""
    return session.get('github_token')


@app.route('/login/user', methods=['GET', 'POST'])
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
    session.pop('github_token', None)
    logout_user()
    return redirect(url_for('main'))

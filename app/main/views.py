from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, LoginForm


@main.route('/')  # , methods=['GET', 'POST'])
def index():
    # print current_user
    return render_template('index.html')

@main.route('/tech')
def tech():
    return render_template('tech.html')


@main.route('/life')
def life():
    return render_template('life.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully.")
            print current_user.username
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

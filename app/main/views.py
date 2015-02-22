from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Permission, Role, User, Post
from ..models import User
from ..email import send_email
from . import main
from .. import db
from .forms import NameForm, LoginForm, PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    # print current_user
    form = PostForm()
    if current_user.can(Permission.WRITE_BLOG) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        # print post.__dict__
        db.session.add(post)
        db.session.commit()
        flash('Post success!')
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, form=form)

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

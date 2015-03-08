from flask import render_template, session, redirect, url_for, abort, flash, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Permission, Role, User, Post
from ..models import User
from ..email import send_email
from . import main
from .. import db
from .forms import NameForm, LoginForm, PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_BLOG) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    tol=form.tol.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('Post success!')
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    for p in posts:
        p.body_preview = p.body if len(p.body) <= 100 else p.body[:100] + '...'
    return render_template('index.html', posts=posts, form=form)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=(post,))


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.tol = form.tol.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    form.tol.data = post.tol
    return render_template('edit_post.html', form=form)

@main.route('/tech')
def tech():
    posts = Post.query.order_by(Post.timestamp.desc()).filter_by(tol='tech')
    return render_template('tech.html', posts=posts)


@main.route('/life')
def life():
    posts = Post.query.order_by(Post.timestamp.desc()).filter_by(tol='life')
    return render_template('life.html', posts=posts)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

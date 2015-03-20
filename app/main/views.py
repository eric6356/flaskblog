from flask import render_template, session, redirect, url_for, abort, flash, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Permission, Role, User, Post
from ..models import User
from ..email import send_email
from . import main
from .. import db
from .forms import NameForm, PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_BLOG) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    tol=form.tol.data,
                    status=int(form.status.data),
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('Post success!')
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc())
    if not current_user.can(Permission.ADMINISTER):
        posts = posts.filter_by(status=1).all()
    else:
        posts = posts.all()
    return render_template('index.html', posts=posts, form=form, preview=True)

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
        post.status = int(form.status.data)
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    form.tol.data = post.tol
    form.status.data = str(post.status)
    return render_template('edit_post.html', form=form)

@main.route('/tech')
def tech():
    posts = Post.query.order_by(Post.timestamp.desc()).filter_by(tol='tech', status=1)
    return render_template('tech.html', posts=posts)


@main.route('/life')
def life():
    posts = Post.query.order_by(Post.timestamp.desc()).filter_by(tol='life', status=1)
    return render_template('life.html', posts=posts)


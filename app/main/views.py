from flask import render_template, session, redirect, url_for, abort, flash, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Permission, Post
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
                    category=form.category.data,
                    status=int(form.status.data),
                    author=current_user._get_current_object(),
                    tags=sorted(form.tags.data.split()))
        post.save()
        flash('Post success!')
        return redirect(url_for('.index'))
    if current_user.can(Permission.ADMINISTER):
        posts = Post.objects.order_by('-timestamp')
    else:
        posts = Post.objects(status=1).order_by('-timestamp')
    for p in posts:
        p.id = str(p.id)
    return render_template('index.html', posts=posts, form=form, preview=True)

@main.route('/post/<id>')
def post(id):
    print id
    post = Post.objects.get_or_404(id=id)
    return render_template('post.html', posts=(post,))


@main.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.objects.get_or_404(id=id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = form.category.data
        post.status = int(form.status.data)
        post.tags = sorted(form.tags.data.split())
        post.save()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    form.category.data = post.category
    form.status.data = str(post.status)
    form.tags.data = ' '.join(sorted(post.tags))
    return render_template('edit_post.html', form=form)

@main.route('/tags/<tag>')
def tags(tag):
    posts = Post.objects(tags=tag)
    return render_template('tags.html', posts=posts, tag=tag)

@main.route('/tech')
def tech():
    posts = Post.objects(category='tech').order_by('-timestamp')
    return render_template('tech.html', posts=posts)


@main.route('/life')
def life():
    posts = Post.objects(category='life').order_by('-timestamp')
    return render_template('life.html', posts=posts)

@main.route('/upload', methods=("GET",))
def upload():
    return render_template('upload.html')

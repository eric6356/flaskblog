# coding: utf-8
from flask import render_template, session, redirect, url_for, abort, flash, request, jsonify, current_app
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Post, Comment, User
from . import api
from collections import Counter
from werkzeug import secure_filename
import os
import datetime
import json
import bleach

@api.route('/hot_tags.json', methods=("GET",))
def hot_tags():
    n = int(request.args.get('n', 3))
    posts = Post.objects.only('tags')
    c = Counter(reduce(list.__add__, (p.tags for p in posts)))
    n = min(n, len(c))
    mc = c.most_common(n)
    return jsonify({'code': 200, 'data': mc})

@api.route('/recent_posts.json', methods=("GET",))
def recent_posts():
    n = int(request.args.get('n', 5))
    posts = Post.objects.only('title').order_by('-timestamp')[:n]
    data = []
    for post in posts:
        p = {'id': str(post.id), 'title': post.title}
        data.append(p)

    res = jsonify({'code': 200, 'data': data})
    return res


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@api.route('/upload.json', methods=("POST", "GET"))
def upload():
    f = request.files['file']
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        print filename
        today = datetime.date.today()
        folder = os.path.join(current_app.config['UPLOAD_FOLDER'], today.strftime('%y/%m/%d'))
        if not os.path.exists(folder):
            os.makedirs(folder)
        f.save(os.path.join(folder, filename))
        url = url_for('static', filename='imgs/' + today.strftime('%y/%m/%d/') + filename)
        return jsonify({'code': 200, 'data': url})
    return jsonify({'code': 400, 'data': 'extension not allowed'})

@api.route('/comment.json', methods=("POST", "PUT"))
def comment():
    post_id = request.form.get('post')
    post = Post.objects.get_or_404(id=post_id)
    commented_id = request.form.get('commented')

    def find_commented(node):
        if str(node.id) == commented_id:
            return node
        for c in node.comments:
            res = find_commented(c)
            if res:
                return res

    if commented_id == post_id:
        if request.method == 'POST':
            commented = post
        elif request.method == 'PUT':
            abort(400)
    else:
        commented = find_commented(post)
        if not commented:
            return jsonify({'code': 400, 'data': 'cannot find commented'})

    if request.method == 'POST':
        content = request.form.get('content')
        author_email = request.form.get('author', 'anonymous@hezj.xyz')
        autor = User.objects.get_or_404(email=author_email)
        content = bleach.clean(content, tags=[], strip=True)
        comment = Comment(author=autor, content=content)

        commented.comments.append(comment)

    elif request.method == 'PUT':
        commented.content = u'This comment has been deleted...'

    post.save()
    return jsonify({'code': 200, 'data': 'ok'})


import flask_moment


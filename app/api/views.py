# coding: utf-8
from flask import render_template, session, redirect, url_for, abort, flash, request, jsonify
from flask.ext.login import login_user, current_user, login_required, logout_user
from ..models import Permission, Post
from ..email import send_email
from . import api
from .. import db
from collections import Counter

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
    print res.data
    return res
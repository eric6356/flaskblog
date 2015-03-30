from . import mongo, login_manager
from flask import current_app, redirect
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import bleach
from markdown import markdown


class Permission:
    WRITE_BLOG = 0x01
    COMMENT = 0x02
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class User(mongo.Document, UserMixin):
    username = mongo.StringField()
    email = mongo.EmailField(primary_key=True)
    password_hash = mongo.StringField()
    isAdmin = mongo.BooleanField(default=False)
    permission = mongo.IntField(default=(Permission.WRITE_BLOG|Permission.COMMENT))
    timestamp = mongo.DateTimeField(default=datetime.utcnow())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if self.email == current_app.config['BLOG_ADMIN']:
            self.isAdmin = True
            self.permission |= Permission.MODERATE_COMMENTS | Permission.ADMINISTER

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def init_user():
        u_admin = User(username='admin', email=current_app.config['BLOG_MAIL_SENDER'], password='admin')
        u_admin.save()

    def can(self, permissions):
        return (self.permission & permissions) == permissions

class AnonymousUser(AnonymousUserMixin):
    username = u"Anonymous"

    def can(self, permissions):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User.objects.with_id(id)
    return user

class Post(mongo.Document):
    title = mongo.StringField()
    body = mongo.StringField()
    status = mongo.IntField(default=1)
    category = mongo.StringField()
    timestamp = mongo.DateTimeField(default=datetime.utcnow)
    author = mongo.ReferenceField(User)

    @property
    def body_html(self):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'del', 'ins']
        return bleach.clean(
            markdown(self.body, ['del_ins'], output_format='html'),
            tags=allowed_tags, strip=True)

    @property
    def body_preview(self):
        res = bleach.clean(self.body_html, tags=[], strip=True)
        return res if len(res) < 200 else res[:200] + '...'

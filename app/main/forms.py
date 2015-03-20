# coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, Length, Email
from flask.ext.pagedown.fields import PageDownField
from ..my_pagedown.fields import PageDownField

class PostForm(Form):
    title = StringField(u'标题', validators=[Required()])
    body = PageDownField(u"正文", validators=[Required()])
    tol = RadioField(u'tol', choices=[('tech', 'Tech'), ('life', 'Life')])
    status = RadioField(u'status', choices=[('1', 'Show'), ('0', 'Hide')], default='1')
    submit = SubmitField('Submit')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

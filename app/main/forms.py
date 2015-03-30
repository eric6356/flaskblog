# coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, Length, Email
from ..my_pagedown.fields import PageDownField

class PostForm(Form):
    title = StringField(u'标题', validators=[Required()])
    body = PageDownField(u"正文", validators=[Required()])
    category = RadioField(u'category', choices=[('tech', 'Tech'), ('life', 'Life')])
    status = RadioField(u'status', choices=[('1', 'Show'), ('0', 'Hide')], default='1')
    tags = StringField()
    submit = SubmitField('Submit')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

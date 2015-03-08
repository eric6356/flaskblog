# coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, Length, Email
from flask.ext.pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField(u'标题', validators=[Required()])
    body = PageDownField(u"正文", validators=[Required()])
    tol = RadioField('tol', choices=[('tech', 'Tech'), ('life', 'Life')])
    submit = SubmitField('Submit')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
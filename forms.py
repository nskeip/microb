#-*- coding: UTF-8 -*-
from wtforms.form import Form
from wtforms.fields import TextField, DateTimeField, TextAreaField, BooleanField

class PostForm(Form):
    title = TextField()
    date = DateTimeField(format='%d/%m/%Y %H:%M:%S')
    text = TextAreaField()
    published = BooleanField()


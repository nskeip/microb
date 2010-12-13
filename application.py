#-*- coding: UTF-8 -*-
import sys
from flask import Flask, render_template, request, url_for, redirect, abort
from db import db_session, Post
from forms import PostForm

import settings

# I just don't know any other ways to fix it to make it
# work with non-ascii characters:(
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           news = Post.query.order_by(Post.date.desc()).\
                                  filter(Post.published==True)[:5])

@app.route('/posts/')
def posts_list():
    return render_template('archive.html',
                           posts = Post.query.order_by(Post.date.desc()).\
                                    filter(Post.published==True))

@app.route('/posts/<int:id>/', methods=['GET', 'POST'])
def post_show(id):
    post = db_session.query(Post).get(id)
    if post is None or not post.published:
        abort(404)
    return render_template('one.html', post=post)

@app.route('/posts/add/', methods=['GET', 'POST'])
@app.route('/posts/<int:id>/edit/', methods=['GET', 'POST'])
def post_add_edit(id=None):

    if id is None:
        # add
        form=PostForm(request.form)
        post=Post()
    else:
        # edit
        post=db_session.query(Post).filter_by(id=id).first()
        if post is None:
            abort(404)
        form=PostForm(request.form, obj=post)        

    if request.method=='POST' and form.validate():
        form.populate_obj(post)
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('index'))

    print form.errors

    return render_template('add_edit.html',
                           form=form,
                           id=id)

@app.route('/posts/<int:id>/delete/', methods=['POST'])
def post_delete(id):
    post = db_session.query(Post).get(id)
    if post is None:
        abort(404)
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.after_request
def remove_db_session(response):
    db_session.remove()
    return response

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)

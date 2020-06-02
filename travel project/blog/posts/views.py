from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@posts.route('/<int:post_id>')
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, date=post.date, post=post)


@posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        return redirect(url_for('posts.read_post', post_id=post_id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text

    return render_template('create_post.html', title='Updating', form=form)


@posts.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('core.index'))
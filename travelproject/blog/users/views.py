from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db
from blog.models import User, Post, Ticket
from blog.users.forms import RegisterForm, LoginForm, UpdateUserForm
from blog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        if User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first():
            flash('This email or username has been already used')
            return render_template('register.html', form=form)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Incorrect email')
            return render_template('login.html', form=form)
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User updated')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename = 'profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@login_required
@users.route('/myinfo')
def my_info():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    profile_image = current_user.profile_image
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.date.asc()).paginate(page=page, per_page=5)
    return render_template('myinfo.html', user=user, profile_image=profile_image, posts=posts, tickets=tickets)









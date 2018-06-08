from flask import render_template, redirect, url_for, flash, request,current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import  _, lazy_gettext as _l
from werkzeug.urls import url_parse
from app.admin import bp

from app.admin.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, PostForm
from app.models import User, Post, Section
from datetime import datetime
from ext import db

from app.admin.email import send_password_reset_email


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))




@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, institute=form.institute.data[0])
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('admin.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_password.html', form=form)


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_adminenticated:
        return redirect(url_for('admin.index'))

    return render_template('admin/admin.html', title=_('Admin'))


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    form = PostForm()
    if form.validate_on_submit():

        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('admin.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('admin.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('admin/index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('admin.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('admin/index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('admin.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('admin/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('admin.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('admin/edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('admin.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('admin.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('admin.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('admin.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('admin.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('admin.user', username=username))



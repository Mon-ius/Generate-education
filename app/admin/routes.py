from flask import render_template, redirect, url_for, flash, request,current_app,abort,jsonify,json
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import  _, lazy_gettext as _l
from werkzeug.urls import url_parse
from app.admin import bp

from app.admin.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, PostForm,EditProfileForm
from app.models import User, Post, Section
from datetime import datetime
from ext import db, photos, sphotos

from app.admin.email import send_password_reset_email


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_adminenticated:
    #     return redirect(url_for('admin.admin'))
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
    # if current_user.is_adminenticated:
    #     return redirect(url_for('admin.admin'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, institute=form.institute.data[0],)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # if current_user.is_adminenticated:
    #     return redirect(url_for('admin.admin'))
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
    # if current_user.is_adminenticated:
    #     return redirect(url_for('admin.admin'))
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
    user_num = len(User.query.filter_by(is_authed=True).all())
    user_num_delay = len(User.query.filter_by(is_authed=False).all())

    post_num = len(Post.query.filter_by(is_authed=True).all())
    post_num_delay = len(Post.query.filter_by(is_authed=False).all())

    return render_template('admin/admin/admin.html', title=_('管理'), user_num=user_num, user_num_delay=user_num_delay, post_num=post_num, post_num_delay=post_num_delay)

@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_adminenticated:
        return redirect(url_for('admin.index'))

    user = User.query.filter_by(is_authed=True).all()
    return render_template('admin/admin/users.html', title=_('认证用户'), users=user)

@bp.route('/users_delay', methods=['GET', 'POST'])
@login_required
def users_delay():
    if not current_user.is_adminenticated:
        return redirect(url_for('admin.index'))

    user_delay = User.query.filter_by(is_authed=False).all()
    return render_template('admin/admin/users.html', title=_('待审核用户'), users=user_delay)

@bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    if not current_user.is_adminenticated:
        return redirect(url_for('admin.index'))

    post = Post.query.filter_by(is_authed=True).all()
    return render_template('admin/admin/posts.html', title=_('上线课程'), posts=post)

@bp.route('/posts_delay', methods=['GET', 'POST'])
@login_required
def posts_delay():
    if not current_user.is_adminenticated:
        return redirect(url_for('admin.index'))

    post_delay = Post.query.filter_by(is_authed=False).all()
    return render_template('admin/admin/posts.html', title=_('待审核课程'), posts=post_delay)


@bp.route('/query/<key>/<value>/<method>')
@login_required
def query(key,value,method):
    
    if not current_user.is_adminenticated:
        abort(400)
    method = bool(int(method))
    if key=='users':
        user = User.query.filter_by(username=value).first_or_404()
        user.is_authed = method
        db.session.commit()

    if key=='posts':
        post = Post.query.filter_by(title=value).first_or_404()
        post.is_authed = method
        print(post.is_authed)
        db.session.commit()
        print(post.is_authed)

    if key=='sections':
        section = Section.query.filter_by(title=value).first_or_404()
        post.is_authed = method
        db.session.commit()

    last_page = 'admin.'+ key
    if(method):
        last_page = last_page+'_delay'
    next_page = url_for(last_page)
    return redirect(next_page)
    

@bp.route('/delete/<username>', methods=['GET', 'POST'])
@login_required
def delete(username):
    if not current_user.is_adminenticated:
        abort(400)
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    print(user.username)
    flash(_('用户删除成功'))
    return redirect(url_for('admin.users'))

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('admin/index.html', title=_('管理首页'), 
                           posts=posts.items)


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    if not current_user.real_name:
        flash(_('完善资料后再试'))
        return redirect(url_for('admin.index'))
    if not current_user.is_authed:
        flash(_('用户信息审核中, 稍后再试'))
        return redirect(url_for('admin.index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data, author=current_user)
        form.photo.data.filename = post.set_photo(
            form.photo.data.filename)
        filename = sphotos.save(form.photo.data)
        file_url = sphotos.url(filename)
        post.set_photo(file_url.split('/')[-1], token=True)
        db.session.add(post)
        db.session.commit()
        flash(_('课程申请已提交'))
        return redirect(url_for('admin.index'))
    return render_template('admin/post.html', title=_('申请课程'),
                           form=form)
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
    if current_user.username == username:
        return redirect(url_for('admin.index'))
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('admin/user.html', user=user)

@bp.route('/courses/<username>')
@login_required
def course(username):
    if current_user.is_adminenticated:
        flash(_('这里不能审核课程!'))
        return redirect(url_for('admin.index'))
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin.course', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('admin.course', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('admin/course.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/view_course/<title>')
@login_required
def view_course(title):
    post = Post.query.filter_by(title=title).first_or_404()
    return render_template('admin/user/view_course.html', post=post)

@bp.route('/edit_course/<title>')
@login_required
def edit_course(title):
    if current_user.is_adminenticated:
        flash(_('这里不能审核课程!'))
        return redirect(url_for('admin.index'))
    post = Post.query.filter_by(title=title).first_or_404()
    if not post.author == current_user:
        flash(_('你没有权限这么做!'))
    return render_template('admin/user/edit_course.html', post=post)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    form = EditProfileForm(current_user.username, current_user.real_name)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.real_name = form.real_name.data
        current_user.about_me = form.about_me.data
        form.photo.data.filename = current_user.set_photo(
            form.photo.data.filename)
        # print(form.photo.data)
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        current_user.set_photo(file_url.split('/')[-1],token=True)
        # print(file_url)
        db.session.commit()
        flash(_('个人信息已更新'))
        return redirect(url_for('admin.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.real_name.data = current_user.real_name or "如:张三"
        form.about_me.data = current_user.about_me
    return render_template('admin/edit_profile.html', title=_('修改资料'),
                           form=form)


@bp.route('/section', methods=['GET', 'POST'])
@login_required
def section():
    if current_user.is_adminenticated:
        return redirect(url_for('admin.admin'))
    if not current_user.real_name:
        flash(_('完善资料后再试'))
        return redirect(url_for('admin.index'))
    if not current_user.is_authed:
        flash(_('用户信息审核中, 稍后再试'))
        return redirect(url_for('admin.index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        form.photo.data.filename = post.set_photo(
            form.photo.data.filename)
        filename = sphotos.save(form.photo.data)
        file_url = sphotos.url(filename)
        post.set_photo(file_url.split('/')[-1], token=True)
        db.session.add(post)
        db.session.commit()
        flash(_('课程申请已提交'))
        return redirect(url_for('admin.index'))
    return render_template('admin/post.html', title=_('添加章节'),
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



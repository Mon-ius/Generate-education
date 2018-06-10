from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User,Post,Section


from ext import INSTITUTIONS, photos, sphotos, videos
# ...
# wtforms.fields.(default field arguments, choices=[], coerce=unicode, option_widget=None)
class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'))
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    institutions = [(ins, ins)
                    for  ins in INSTITUTIONS]
    
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])

    institute = SelectMultipleField(
        _l('学院'),[], choices=institutions, 
        render_kw={"multiple": "multiple"})

    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('重复密码'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('注册'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('该用户名已被占用'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('该邮箱已被使用.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('重置密码'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('重复密码'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('重置'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    real_name = StringField(_l('真实姓名'), validators=[DataRequired()])
    about_me = TextAreaField(_l('个人简介'),
                             validators=[Length(min=0, max=140)])
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, original_real_name, * args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_real_name = original_real_name

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('此用户名已被占用'))


class PostForm(FlaskForm):
    title = StringField(_l('课程名称'), validators=[DataRequired()])
    body = TextAreaField(_l('课程简介'),
                             validators=[Length(min=0, max=150)])
    photo = FileField(validators=[
        FileAllowed(sphotos, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])

    submit = SubmitField(_l('课程申请'))

    def validate_post(self, post):
        post = Post.query.filter_by(title=self.title.data).first()
        if post is not None:
            raise ValidationError(_('此课程名已被占用'))

class SectForm(FlaskForm):
    title = StringField(_l('课程名称'), validators=[DataRequired()])
    body = TextAreaField(_l('课程简介'),
                             validators=[Length(min=0, max=150)])
    photo = FileField(validators=[
        FileAllowed(sphotos, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])

    video = FileField(validators=[
        FileAllowed(videos, u'只能上传视频！'),
        FileRequired(u'文件未选择！')])

    submit = SubmitField(_l('章节申请'))

    def validate_post(self, post):
        section = Section.query.filter_by(title=self.title.data).first()
        if section is not None:
            raise ValidationError(_('此章节名已被占用'))


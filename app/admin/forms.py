from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User,Post,Section

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from ext import INSTITUTIONS
# ...
# wtforms.fields.(default field arguments, choices=[], coerce=unicode, option_widget=None)
class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'))
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    institutions = [(str(i), ins)
                    for i, ins in enumerate(INSTITUTIONS)]
    
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
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


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
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

from flask import render_template, redirect, url_for, flash, request
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from flask_images import resized_img_src
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('main/index.html', title=_('Home'),main='active')




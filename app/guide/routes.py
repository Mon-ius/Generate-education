from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_babel import _, lazy_gettext as _l
from app.guide import bp


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('guide/index.html', title=_('工作指南'), guide='active')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('guide/contact.html', title=_('联系我们'), guide='active')


@bp.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('guide/success.html', title=_('提交成功'), guide='active')

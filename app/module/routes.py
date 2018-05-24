from flask import render_template, redirect, url_for, flash, request,jsonify
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.module import bp

import numpy as np
from functools import reduce
@bp.route('/module', methods=['GET', 'POST'])
def  index():

    return render_template('module/index.html', title=_('模块与课程'), module='active')

import os
from flask import Flask, request, current_app

from ext import db, migrate, bootstrap, babel, Config, images, cache, login, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config['SECRET_KEY']='dai3hoahudhiuahduiah'
    # app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'
    app.config.from_object(config_class)

    db.init_app(app)  # SQLite初始化
    migrate.init_app(app, db)  # 数据库迁移初始化
    bootstrap.init_app(app)  # Bootstrap初始化
    babel.init_app(app)  # I18nL10n 初始化
    images.init_app(app)  # Imagine Normalise 初始化
    login.init_app(app)  # 用户系统 初始化
    login.login_view = 'admin.login'
    mail.init_app(app)  # 邮件系统 初始化
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})  # 页面缓存 初始化
    
    from app.main import bp as main_bp  # 首页注册
    app.register_blueprint(main_bp)
    
    from app.module import bp as module_bp  # 课程模块注册
    app.register_blueprint(module_bp)

    from app.experiment import bp as experiment_bp  # 通识实验注册
    app.register_blueprint(experiment_bp, url_prefix='/experiment')

    from app.guide import bp as guide_bp  # 课程指南注册
    app.register_blueprint(guide_bp, url_prefix='/guide')

    from app.admin import bp as admin_bp  # 管理页面注册
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.errors import bp as errors_bp #错误处理页面注册
    app.register_blueprint(errors_bp)
    
    return app




from app import models

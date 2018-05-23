from flask import Blueprint

bp = Blueprint('module', __name__)

from app.module import routes
from flask import Blueprint

bp = Blueprint('guide', __name__)

from app.guide import routes

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_images import Images
from flask_cache import Cache
from flask_babel import Babel, _, lazy_gettext as _l
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
cache = Cache()
babel = Babel()
images = Images()
desc = sqlalchemy.desc



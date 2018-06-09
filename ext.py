import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_images import Images
from flask_cache import Cache
from flask_babel import Babel,_, lazy_gettext as _l
from flask_mail import Mail
from config import Config
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
cache = Cache()
babel = Babel()
images = Images()
login = LoginManager()
mail = Mail()
photos = UploadSet('photos', IMAGES)
desc = sqlalchemy.desc
INSTITUTIONS = ["信息工程学院", "新闻与传媒学院", "广陵学院", " 文学院", "社会发展学院", "物理科学与技术学院",
"化学化工学院","教育科学学院（师范学院）","学前教育学院","数学科学学院"," 马克思主义学院","农学院",
"园艺与植物保护学院","音乐学院","美术与设计学院","兽医学院","动物科学与技术学院","生物科学与技术学院",
" 医学院","护理学院"," 旅游烹饪学院","水利与能源动力工程学院","环境科学与工程学院","机械工程学院",
"法学院","商学院","外国语学院","建筑科学与工程学院","体育学院"," 广陵学院","创新创业学院"]


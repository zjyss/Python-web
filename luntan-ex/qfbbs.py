from flask import Flask
from apps.cms.views import bp as cms_bp
from apps.common.views import common
from apps.front.views import front
import config
from exts import db,mail
from apps.cms.models import User
from apps.front.models import FUser
from apps.models import PostsModel


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front)
    app.register_blueprint(common)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    app.config['SECRET_KEY'] = '110'
    return app

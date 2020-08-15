from flask import Flask


def create_app():
    app = Flask(__name__)

    from wechat_api import api
    app.register_blueprint(api)
    return app
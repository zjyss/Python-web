from flask import Blueprint

api = Blueprint('wechat_api', __name__, url_prefix='/api/v1.0/wechat')


from . import chat_api

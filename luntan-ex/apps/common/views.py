from io import BytesIO

from flask import Blueprint, make_response

from utils import bbs_cache
from utils.captcha import Captcha

common = Blueprint('common', __name__, url_prefix='/common')



# 图片验证码
@common.route('/capture/')
def capture():
    text, image = Captcha.gene_graph_captcha()
    # 存入memcache缓存
    bbs_cache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)

    respon = make_response(out.read())
    respon.content_type = 'imge/png'
    return respon

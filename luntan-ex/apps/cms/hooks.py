from .models import User, CmsUserPermission
from flask import g, session
import config
from .views import bp


@bp.before_request
def before_request():
    if config.SESSION_KEEPUSER in session:
        user_id = session.get(config.SESSION_KEEPUSER)
        user = User.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def context_processor():
    return {'CmsUserPermission':CmsUserPermission}


# @bp.app_errorhandler(404)
# # def error_page(error):
# #     print(2313321321323232313132)
# #     return render_template('cms/404.html'),404

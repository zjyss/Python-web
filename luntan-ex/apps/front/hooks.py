from flask import g, session
from .views import front
import config
from .models import FUser

@front.before_request
def before_request():
    user_id = session.get(config.SESSION_FRONT_KEEPUSER)
    user = FUser.query.get(user_id)
    if user:
        g.front_user = user

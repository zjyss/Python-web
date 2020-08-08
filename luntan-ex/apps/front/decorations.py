from functools import wraps
from flask import session, redirect, url_for
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.SESSION_FRONT_KEEPUSER in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.login'))
    return inner
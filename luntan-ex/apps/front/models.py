from datetime import datetime

from exts import db


class FUser(db.Model):
    __tablename__ = 'fuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    # sex = db.Column(db.Boolean, nullable=False)
    phone = db.Column(db.String(32), nullable=False, unique=True)
    join_time = db.Column(db.DATETIME, default=datetime.now)

from datetime import datetime

from exts import db


class BoardsModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


class PostsModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    common_totle = db.Column(db.Integer, default=0)
    dianzan_totle = db.Column(db.Integer,default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('fuser.id'), nullable=False)

    board = db.relationship('BoardsModel', backref='posts')
    author = db.relationship('FUser', backref='posts')


# 帖子加精
class HighLightPostModel(db.Model):
    __tablename__ = 'highlight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    creat_time = db.Column(db.DateTime, default=datetime.now)
    post = db.relationship('PostsModel', backref='highlight')


# 评论
class CommonModel(db.Model):
    __tablename__ = 'common'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('fuser.id'))
    post = db.relationship('PostsModel', backref='commons')
    author = db.relationship('FUser', backref='commons')


class DianZanModel(db.Model):
    __tablename__ = 'dianzan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('fuser.id'))
    post = db.relationship('PostsModel', backref='dianzans')
    author = db.relationship('FUser', backref='dianzans')

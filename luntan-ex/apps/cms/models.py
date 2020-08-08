from datetime import datetime

from exts import db


class CmsUserPermission(object):
    ALL_PERMISSIONS = 0b11111111
    # 访客
    VISITOR = 0b00000001
    # 帖子管理
    POSTER = 0b00000010
    # 评论
    COMMENTOR = 0b00000100
    # 板块
    BOARDER = 0b00001000
    # 前台用户管理
    FRONTUSER = 0b00010000
    # 后台用户管理
    CMSUSER = 0b00100000
    # 管理员
    ADMINISTRATOR = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cmsrole_id', db.Integer, db.ForeignKey('cmsrole.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class CmsRole(db.Model):
    __tablename__ = 'cmsrole'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CmsUserPermission.VISITOR)

    users = db.relationship('User', secondary=cms_role_user, backref='cmsroles')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, default='admin')
    password = db.Column(db.String(30), nullable=False)
    e_mail = db.Column(db.String(100), unique=True, nullable=False)
    join_time = db.Column(db.DATETIME, default=datetime.now)

    @property
    def permissions(self):
        if self.cmsroles:
            print(111)
            return 0
        all_permissions = 0
        for role in self.cmsroles:
            permission = role.permissions
            all_permissions |= permission
        return all_permissions

    def check_permission(self, permission):
        # for role in self.cmsroles:
        #     print(role.permissions)
        print(self.permissions, permission)
        return self.permissions & permission == permission

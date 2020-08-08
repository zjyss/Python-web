from qfbbs import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from apps.cms.models import User, CmsRole, CmsUserPermission

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-n', '--username', dest='username')
def creaate_super_user(email, password, username):
    user = User(e_mail=email, password=password, username=username)
    db.session.add(user)
    db.session.commit()


@manager.command
def create_role():
    # 1访问者
    vistor = CmsRole(name='访问者', desc='只能看，不能改')
    vistor.permissions = CmsUserPermission.VISITOR
    # 运营部门  改个人信息  管理帖子 管理评论  管理前台用户
    operator = CmsRole(name='运营人员', desc='管理帖子、管理评论、管理前台用户')
    operator.permissions = CmsUserPermission.VISITOR | CmsUserPermission.POSTER | CmsUserPermission.COMMENTOR | CmsUserPermission.FRONTUSER
    # 管理部门
    administrator = CmsRole(name='管理人员', desc='拥有本系统所有的权限')
    administrator.permissions = CmsUserPermission.VISITOR | CmsUserPermission.POSTER | CmsUserPermission.COMMENTOR | CmsUserPermission.FRONTUSER | CmsUserPermission.BOARDER | CmsUserPermission.CMSUSER

    # 开发部门
    developer = CmsRole(name='开发', desc='开发人员专用权限')
    developer.permissions = CmsUserPermission.ALL_PERMISSIONS

    db.session.add_all([vistor, operator, administrator, developer])
    db.session.commit()
    print('角色创建成功')


@manager.option('-e', '--email', dest="email")
@manager.option('-n', '--name', dest="name")
def add_user_to_role(email, name):
    user = User.query.filter(User.e_mail == email).first()
    if user:
        role = CmsRole.query.filter(CmsRole.name == name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print(f'{user.username}添加{role.name}权限到成功')
        else:
            print('没有那个权限')
    else:
        print('没有找到用户')


@manager.command
def test_permissions():
    user = User.query.filter(User.e_mail == '19972664696@163.com').first()
    if user.check_permission(CmsUserPermission.COMMENTOR):
        print('该用户有这个权限')
    else:
        print('该用户没有权限')


if __name__ == '__main__':
    manager.run()

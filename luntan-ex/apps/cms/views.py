import random
import string
from flask import Blueprint, render_template, request, views, session, redirect, url_for, g
# from apps.form import BaseForm
from exts import db,mail
from .forms import LoginForm, RestPassword, ResetEmail, AddBoard
from .models import User
import config
from utils import restful
from flask_mail import Message
from utils import bbs_cache
from .decorations import login_required
from apps.models import BoardsModel, PostsModel, HighLightPostModel
from celery_tasks import sendmail
bp = Blueprint('cms', __name__, url_prefix='/cms')

# 后台首页
@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

# 后台登陆视图
class LoginView(views.MethodView):
    def get(self):
        return render_template('cms/cms_login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            password = form.password.data
            email = form.email.data
            user = User.query.filter_by(e_mail=email).first()
            if user and user.password == password:
                # 登陆成功，设置session
                session[config.SESSION_KEEPUSER] = user.id
                print(session.get(config.SESSION_KEEPUSER))
                return redirect(url_for('cms.index'))
            else:
                return redirect(url_for('cms.login'))
        else:
            return redirect(url_for('cms.login'))

# 重置密码视图
class RestpaView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpasswd.html')

    def post(self):
        form = RestPassword(request.form)
        print(form.validate())
        if form.validate():
            oldpassword = form.oldpassword.data
            newpassword = form.newpassword.data
            print(oldpassword, newpassword)
            user = g.cms_user
            if user.password == oldpassword:
                user.password = newpassword
                db.session.commit()
                return restful.success('修改密码成功')
            else:
                return restful.parms_error('旧密码错误')
        else:
            return restful.parms_error(form.get_errors())

# 等出
@bp.route('logout')
@login_required
def logout():
    del session[config.SESSION_KEEPUSER]
    return redirect(url_for('cms.login'))

# 个人信息
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('cms/cms_profile.html')

# 设置邮箱验证码/发下哦那个邮件
@bp.route('/email_capture', methods=['GET', 'POST'])
@login_required
def email_capture():
    email = request.form.get('email')
    print(email)
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    em_capture = ''.join(random.sample(source, 6))
    print(em_capture)
    message = Message('邮箱验证码', recipients=[email], body='验证码是：%s' % em_capture)
    mail.send(message=message)
    # sendmail.daly('邮箱验证码', recipients=[email], body='验证码是：%s' % em_capture)
    bbs_cache.set(email, em_capture)
    return restful.success('发送成功')

# 修改邮箱操作
class ResetEmailView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmail(request.form)
        print(form.validate())
        if form.validate():
            email = form.email.data
            g.cms_user.e_mail = email
            db.session.commit()
            return restful.success('chenggong')
        else:
            return restful.parms_error('cuowu')

# 添加板块
@bp.route('/addboard/', methods=['POST', 'GET'])
def addboard():
    form = AddBoard(request.form)
    if form.validate():
        name = form.name.data
        #     添加模块名
        board = BoardsModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success('添加成功')
    return restful.parms_error('添加失败')

# 板块页面/查看所有板块
@bp.route('/board/', methods=['GET'])
def board():
    boards = BoardsModel.query.all()
    context = {
        'boards': boards
    }
    return render_template('cms/cms_boards.html', **context)

# 删除板块
@bp.route('/delete_board/', methods=['POST', 'GET'])
def delete_board():
    id = request.form.get('id')
    board = BoardsModel.query.get(id)
    db.session.delete(board)
    db.session.commit()
    return restful.success('删除成功')

# 修改板块
@bp.route('/edit_board/', methods=['POST', 'GET'])
def edit_board():
    id = request.form.get('id')
    name = request.form.get('name')
    board = BoardsModel.query.get(id)
    board.name = name
    db.session.commit()
    return restful.success('修改成功')

# 删除帖子
@bp.route('/delete_post/', methods=['POST', 'GET'])
@login_required
def delete_post():
    if request.method == 'GET':
        posts = PostsModel.query.all()
        context = {
            'posts': posts
        }
        return render_template('cms/cms_posts.html', **context)
    else:
        post_id = request.form.get('post_id')
        post = PostsModel.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return restful.success('删除成功')
        else:
            return restful.parms_error('帖子不存在')

# 贴子加精
@bp.route('/good_post/')
@login_required
def good_post():
    post_id = request.args.get('post_id')
    post = PostsModel.query.get(post_id)
    print(post_id)
    if post_id:
        highligth = HighLightPostModel(post=post)
        db.session.add(highligth)
        db.session.commit()
        return restful.success('加精成功')
    else:
        return restful.parms_error('加精失败')

# 取消加精
@bp.route('/un_good_post/')
@login_required
def un_good_post():
    post_id = request.args.get('post_id')
    post = PostsModel.query.get(post_id)
    if post_id:
        highligth = HighLightPostModel.query.filter_by(post_id=post_id).first()
        db.session.delete(highligth)
        db.session.commit()
        return restful.success('取消加精成功')
    else:
        return restful.parms_error('取消加精失败')


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpassword/', view_func=RestpaView.as_view('resetpassword'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

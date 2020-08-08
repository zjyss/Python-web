from flask import Blueprint, render_template, views, request, redirect, url_for, session, g
import config
from apps.front.forms import RegisterForm, LoginForm, AddPostForm, CommonForm
from apps.front.models import FUser
from apps.models import BoardsModel, PostsModel, CommonModel, DianZanModel
from exts import db
from utils import restful
from .decorations import login_required
from flask_paginate import Pagination, get_per_page_parameter

front = Blueprint('front', __name__, url_prefix='/front')


# 首页
@front.route('/', methods=['GET', 'POST'])
@front.route('/index/')
def index():
    dianzans = DianZanModel.query.filter(DianZanModel.author == g.front_user)
    post_id_list = []
    for i in dianzans:
        post_id_list.append(i.post_id)
    boards = BoardsModel.query.all()
    posts = PostsModel.query.order_by(PostsModel.create_time.desc())
    # 分页
    page = request.args.get(get_per_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    totle = PostsModel.query.count()
    pagination = Pagination(page=page, bs_version=3, total=totle, outer_window=1, inner_window=2)
    st = request.args.get('st')
    if st == '2':
        posts = PostsModel.query.filter(PostsModel.highlight)
        context = {
            'boards': boards,
            'posts': posts,
            'pagination': pagination,
            'post_id_list': post_id_list
        }
        return render_template('front/index.html', **context)
    if st == '3':
        posts = PostsModel.query.order_by(PostsModel.dianzan_totle.desc()).slice(0, 10)
        context = {
            'boards': boards,
            'posts': posts,
            'pagination': pagination,
            'post_id_list': post_id_list
        }
        return render_template('front/index.html', **context)
    if st == '4':
        posts = PostsModel.query.order_by(PostsModel.common_totle.desc()).slice(0, 10)
        context = {
            'boards': boards,
            'posts': posts,
            'pagination': pagination,
            'post_id_list': post_id_list
        }
        return render_template('front/index.html', **context)
    board_id = request.args.get('board_id')
    if board_id:
        posts = PostsModel.query.filter(PostsModel.board_id == board_id)
        posts_totle = posts.slice(start, end)
        context = {
            'boards': boards,
            'posts': posts_totle,
            'pagination': pagination,
            'post_id_list': post_id_list
        }
        return render_template('front/index.html', **context)

    context = {
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'post_id_list': post_id_list
    }

    return render_template('front/index.html', **context)


# 注册视图
class RegisterView(views.MethodView):
    def get(self):
        return render_template('front/register.html')

    def post(self):
        form = RegisterForm(request.form)
        print(form.validate())
        if form.validate():
            print(222)
            username = form.username.data
            password = form.password.data
            phone = form.phone.data
            user = FUser(name=username, password=password, phone=phone)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('front.index'))
        else:
            return redirect(url_for('front.register'))


# 登陆视图
class LoginView(views.MethodView):
    def get(self):
        return render_template('front/login.html')

    def post(self):
        print(222)
        form = LoginForm(request.form)
        if form.validate():
            print(111)
            username = form.username.data
            password = form.password.data
            user = FUser.query.filter(FUser.name == username).first()
            if user:
                if user.password == password:
                    session[config.SESSION_FRONT_KEEPUSER] = user.id
                    return redirect(url_for('front.index'))
                else:
                    return redirect(url_for('front.login'))
            else:
                return redirect(url_for('front.login'))


# 退出登陆
@front.route('/logout/')
@login_required
def logout():
    del session[config.SESSION_FRONT_KEEPUSER]
    return redirect(url_for('front.login'))


# 发帖
@front.route('/apost/', methods=['POST', 'GET'])
@login_required
def addpost():
    if request.method == 'GET':
        boards = BoardsModel.query.all()
        context = {
            'boards': boards
        }
        return render_template('front/front_post.html', **context)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            content = form.content.data

            #             1111
            post = PostsModel(title=title, content=content)
            post.board_id = board_id
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success('发帖成功')
        else:
            return restful.parms_error('发帖失败')


# 查看文章内容
@front.route('/detail/')
def detail():
    post_id = request.args.get('post_id')
    commons = CommonModel.query.filter(CommonModel.post_id == post_id)
    post = PostsModel.query.get(post_id)
    boards = BoardsModel.query.all()
    context = {
        'post': post,
        'commons': commons,
        'boards': boards
    }
    return render_template('front/front_pdetail.html', **context)


# 添加评论
@front.route('/common/')
@login_required
def common():
    form = CommonForm(request.args)
    if form.validate():
        post_id = form.post_id.data
        post = PostsModel.query.get(post_id)
        post.common_totle += 1
        content = form.content.data
        # print(post_id,content[3:-4])
        content = CommonModel(content=content)
        content.post_id = post_id
        content.author = g.front_user
        db.session.add(content)
        db.session.commit()
        return restful.success('评论成功')
    return restful.success('评论失败')


# 查询
@front.route('/search/', methods=['POST', 'GET'])
def search():
    search_tips = request.args.get('search_tips')
    print(search_tips)
    posts = PostsModel.query.filter(PostsModel.title.contains(search_tips))
    print(posts)
    # 分页
    # page = request.args.get(get_per_page_parameter(), type=int, default=1)
    # start = (page - 1) * config.PER_PAGE
    # end = start + config.PER_PAGE
    # totle = PostsModel.query.count()
    # pagination = Pagination(page=page, bs_version=3, total=totle, outer_window=1, inner_window=2)
    context = {
        'posts': posts,
        # 'pagination':pagination
    }
    return render_template('front/search.html', **context)


# 点赞
@front.route('/dianzan/')
@login_required
def dianzan():
    flag = 0
    post_id = request.args.get('post_id')
    post = PostsModel.query.get(post_id)
    # dianzan_find = DianZanModel.query.filter(
    #     DianZanModel.post_id == post_id).filter(DianZanModel.author_id == g.front_user.id).first()
    # if dianzan_find:
    #     flag = 1
    post.dianzan_totle += 1
    dianzan_nos = DianZanModel(post=post, author=g.front_user)
    db.session.add(dianzan_nos)
    db.session.commit()
    return restful.success('成功')


# 取消点赞
@front.route('/cancel_dianzan/')
@login_required
def cancel_dianzan():
    post_id = request.args.get('post_id')
    post = PostsModel.query.get(post_id)
    post.dianzan_totle -= 1
    dianzan = DianZanModel.query.filter(DianZanModel.post == post).filter(DianZanModel.author == g.front_user).first()
    db.session.delete(dianzan)
    db.session.commit()
    return restful.success('成功')


# 个人中心
@front.route('/user_info/')
@login_required
def user_info():
    st = request.args.get('st')
    if st == '1':
        posts = PostsModel.query.filter(PostsModel.author == g.front_user)
        context = {
            'posts': posts
        }
    elif st == '2':
        dianzans = DianZanModel.query.filter(DianZanModel.author == g.front_user)
        context = {
            'dianzans': dianzans,
            'flag': 1
        }
    else:
        posts = PostsModel.query.filter(PostsModel.author == g.front_user)
        context = {
            'posts': posts
        }
    return render_template('front/user_info.html', **context)


front.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
front.add_url_rule('/login/', view_func=LoginView.as_view('login'))

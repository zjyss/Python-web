from apps.form import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length, InputRequired, Regexp, ValidationError
import utils.bbs_cache


class RegisterForm(BaseForm):
    username = StringField(validators=[Length(3, 8, message='用户名不符合规范'), InputRequired(message='输入用户名')])
    password = StringField(validators=[Length(3, 8, message='密码不符合规范'), InputRequired(message='输入密码')])
    phone = StringField(validators=[Length(9, 12, message='手机号不符合规范')])
    img_grapth = StringField(validators=[Regexp(r'\w{4}', message='输入争取的验证码')])

    def validate_img_grapth(self, field):
        img_graph = field.data
        if img_graph:
            if not utils.bbs_cache.get(img_graph.lower()):
                raise ValidationError(message='验证码错误')


class LoginForm(BaseForm):
    username = StringField(validators=[Length(3, 8, message='用户名不符合规范'), InputRequired(message='输入用户名')])
    password = StringField(validators=[Length(3, 8, message='密码不符合规范'), InputRequired(message='输入密码')])


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='输入标题')])
    content = StringField(validators=[InputRequired(message='输入内容')])
    board_id = StringField(validators=[InputRequired(message='选择板块')])

# 评论
class CommonForm(BaseForm):
    post_id = StringField(validators=[InputRequired(message='输入id')])
    content = StringField(validators=[InputRequired(message='输入内容')])
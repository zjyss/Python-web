from wtforms import Form
from apps.form import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, ValidationError
from utils import bbs_cache
from flask import g


class LoginForm(BaseForm):
    # username = StringField(validators=[Length(3, 6, message='输入正确的用户名'), InputRequired(message='输入用户名')])
    email = StringField(validators=[Email(message='输入正确的email地址'), InputRequired(message='输入邮箱')])
    password = StringField(validators=[Length(3, 8, message='输入正确的密码格式')])


class RestPassword(BaseForm):
    oldpassword = StringField(validators=[Length(3, 8, message='输入正确格式的密码')])
    newpassword = StringField(validators=[Length(3, 8, message='输入正确格式的密码')])
    newpassword2 = StringField(validators=[EqualTo("newpassword", message="两次密码必须一致")])


class ResetEmail(BaseForm):
    email = StringField(validators=[Email(message='输入正确的邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='输入正确长度的验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = bbs_cache.get(email)
        if not captcha or captcha_cache.lower() != captcha.lower():
            raise ValidationError(message='验证码错误')

    def validate_email(self, field):
        email = field.data
        if g.cms_user.e_mail == email:
            raise ValidationError(message='不能和原邮箱一样')


class AddBoard(BaseForm):
    name = StringField(validators=[Length(3, 7, message='输入模块名')])

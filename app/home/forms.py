# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号！")
        ],
        description='账号',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入账号！"

        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱！"),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！"
        }
    )

    phone = StringField(
        label='手机',
        validators=[
            DataRequired("请输入手机！"),
            Regexp("1[345789]\\d{9}", message='手机号码不正确！')
        ],
        description='手机',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机！"
        }
    )

    pwd = PasswordField(
        label='密码',  # 标签,展示在浏览器页面的字符串信息，如登录按钮中的‘登录’二字
        validators=[  # 验证器
            DataRequired("请输入密码！")
        ],
        description='密码',  # 描述
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！"
            # "required": "required"  # 必填项
        }

    )

    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message='两次密码不一致！')
        ],
        description='确认密码',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码！"
        }

    )

    submit = SubmitField(
        label='注册',
        render_kw={
            "id": "btn-sub",
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user >= 1:
            raise ValidationError('昵称已存在')

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user >= 1:
            raise ValidationError('邮箱已存在')

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user >= 1:
            raise ValidationError('手机号已存在')


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号！")
        ],
        description='账号',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入账号！"

        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！"
        }
    )

    submit = SubmitField(
        label='登录',
        render_kw={
            "id": "btn-sub",
            "class": "btn btn-lg btn-success btn-block",
        }
    )


class UserdetailForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired("账号不能为空！")
        ],
        description='账号',
        render_kw={
            "class": "form-control",
            "placeholder": "账号不能为空！"

        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("邮箱不能为空！"),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            "class": "form-control",
            "placeholder": "邮箱不能为空！"
        }
    )

    phone = StringField(
        label='手机',
        validators=[
            DataRequired("请输入手机！"),
            Regexp("1[345789]\\d{9}", message='手机号码不正确！')
        ],
        description='手机',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机！"
        }
    )

    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像！')
        ],
        description='头像'
    )

    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("简介不能为空")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows=": 10,
        }
    )

    submit = SubmitField(
        label='保存修改',
        render_kw={
            "class": "btn btn-success",
        }
    )



# 修改密码
class PwdFrom(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('旧密码不能为空！')
        ],
        description='旧密码',
        render_kw={
            "type": "password",
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入旧密码！"
        }
    )

    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('新密码不能为空！')
        ],
        description='新密码',
        render_kw={
            "class": "form-control",
            "id": "input_newpwd",
            "placeholder": "请输入新密码！"
        }
    )

    submit = SubmitField(
        label='修改',
        render_kw={
            "class": "btn btn-success"
        }
    )

    # 修改密码时，验证旧密码是否正确
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session['user']
        user = User.query.filter_by(name=name).first()
        if not user.check_pwd(pwd):
            raise ValidationError('旧密码输入错误！')


class CommentForm(FlaskForm):
    content=TextAreaField(
        label='内容',
        validators=[
            DataRequired('请输入内容！')
        ],
        description='内容',
        render_kw={
            "id": "input_content"
        }
    )

    submit = SubmitField(
        label='提交评论',
        render_kw={
            "class": "btn btn-success",
            "id":"btn-sub"
        }
    )
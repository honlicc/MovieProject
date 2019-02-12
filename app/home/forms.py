# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
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

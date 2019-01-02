# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    '''管理员登录表单'''
    account = StringField(
        label='账号',  # 标签
        validators=[  # 验证器
            DataRequired("请输入账号！")
        ],
        description='账号',  # 描述
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            #"required": "required"  # 必填项
        }
    )

    pwd = PasswordField(
        label='密码',  # 标签,展示在浏览器页面的字符串信息，如登录按钮中的‘登录’二字
        validators=[  # 验证器
            DataRequired("请输入密码！")
        ],
        description='密码',  # 描述
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            #"required": "required"  # 必填项
        }

    )

    submit = SubmitField(
        label='登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

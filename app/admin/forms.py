# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,ValidationError
from app.models import *


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
            "placeholder": "请输入账号！"
            # "required": "required"  # 必填项

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
            "placeholder": "请输入密码！"
            # "required": "required"  # 必填项
        }

    )

    submit = SubmitField(
        '登录',
        render_kw={
            "id": "btn-sub",
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    #验证器：
    def validate_account(self,request):
        account=request.data    #获取请求账号数据
        admin=Admin.query.filter_by(name=account).first()
        if not admin:
            raise ValidationError("账号不存在！")



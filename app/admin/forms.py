# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import *

tags = Tag.query.all()


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
        label='登录',
        render_kw={
            "id": "btn-sub",
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证器：
    def validate_account(self, request):
        account = request.data  # 获取请求账号数据
        admin = Admin.query.filter_by(name=account).first()
        if not admin:
            raise ValidationError("账号不存在！")


class TagFrom(FlaskForm):
    name = StringField(
        label='标签',
        validators=[
            DataRequired('请输入标签！')
        ],
        description='标签',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )

    submit = SubmitField(
        label='确定',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MoiveForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名！')
        ],
        description='片名',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名！"
        }
    )

    url = FileField(
        label='文件',
        validators=[
            DataRequired('请上传文件！')
        ],
        description='文件'
    )

    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            "class": "form-control",
            "rows": 10,
            "placeholder": "请输入简介！"
        }
    )

    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面！')
        ],
        description='封面',
    )

    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        description='星级',
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )

    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired('请选择标签！')
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description='标签',
        render_kw={
            "class": "form-control",
        }
    )

    area = StringField(
        label='地区',
        validators=[
            DataRequired('请输入地区！')
        ],
        description='地区',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )

    length = StringField(
        label='片长',
        validators=[
            DataRequired('请输入片长！')
        ],
        description='片长',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )

    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired('请选择上映时间！')
        ],
        description='上映时间',
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time",
            "placeholder": "请选择上映时间！"
        }
    )

    submit = SubmitField(
        label='确定',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired('预告标题不能为空!')
        ],
        description='预告标题',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请上传预告标题！"
        }
    )

    logo = FileField(
        label='预告封面',
        validators=[
            DataRequired('预告封面不能为空!')
        ],
        description='预告封面',
    )

    submit = SubmitField(
        label='确定',
        render_kw={
            "class": "btn btn-primary",
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
        label='确定',
        render_kw={
            "class": "btn btn-primary"
        }
    )

    #修改密码时，验证旧密码是否正确
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session['admin']
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError('旧密码输入错误！')


class AuthFrom(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('权限名称不能为空！')
        ],
        description='权限名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )

    url = StringField(
        label='权限地址',
        validators=[
            DataRequired('权限地址不能为空！')
        ],
        description='权限地址名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限地址！"
        }
    )

    submit = SubmitField(
        label='确定',
        render_kw={
            "class": "btn btn-primary"
        }
    )
from flask import render_template, redirect, url_for, request

from . import admin
from app.admin.forms import LoginForm


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()  # 表单实例化
    if form.validate_on_submit():
        data = form.data  # 获取数据
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
def logout():
    return redirect(url_for('admin/login'))


@admin.route('/pwd/')
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/add/')
def tag_add():
    return render_template('admin/tag_add.html')


@admin.route('/tag/list/')
def tag_list():
    return render_template('admin/tag_list.html')


@admin.route('/movie/add/')
def movie_add():
    return render_template('admin/movie_add.html')


@admin.route('/movie/list/')
def movie_list():
    return render_template('admin/movie_list.html')


@admin.route('/preview/add/')
def preview_add():
    return render_template('admin/preview_add.html')


@admin.route('/preview/list/')
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admin.route('/user/list/')
def user_list():
    return render_template('admin/user_list.html')


# 会员详情
@admin.route('/user/view/')
def user_view():
    return render_template('admin/user_view.html')


# 评论列表
@admin.route('/comment/list/')
def comment_list():
    return render_template('admin/comment_list.html')


# 电影收藏
@admin.route('/moviecol/list/')
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 操作日志
@admin.route('/oplog/list/')
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登录日志
@admin.route('/adminloginlog/list/')
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志
@admin.route('/userloginlog/list/')
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 权限添加
@admin.route('/auth/add/')
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin.route('/auth/list/')
def auth_list():
    return render_template('admin/auth_list.html')


# 角色添加
@admin.route('/role/add/')
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admin.route('/role/list/')
def role_list():
    return render_template('admin/role_list.html')


# 管理员添加
@admin.route('/admin/add/')
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin/list/')
def admin_list():
    return render_template('admin/admin_list.html')

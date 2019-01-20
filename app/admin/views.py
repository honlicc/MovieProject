from flask import render_template, redirect, url_for, flash, session, request, make_response

from app import db
from app.models import Admin, Tag, Movie
from . import admin
from app.admin.forms import LoginForm, TagFrom, MoveForm
from functools import wraps
from app import app
from werkzeug.utils import secure_filename
import uuid
import os
import datetime


# 访问控制装饰器
def admin_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改问价名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route('/')
@admin_login
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()  # 表单实例化
    if form.validate_on_submit():
        data = form.data  # 获取数据
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        resp = session.get('admin')
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
@admin_login
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin/login'))


@admin.route('/pwd/')
@admin_login
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login
def tag_add():
    form = TagFrom()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('标签已存在', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('标签添加成功', 'ok')
        redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/list/<int:page>/', methods=["GET"])
@admin_login
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 删除tag
@admin.route('/tag/del/<int:id>/', methods=["GET"])
@admin_login
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 编辑tag
@admin.route('/tag/edit/<int:id>/', methods=["GET", "POST"])
@admin_login
def tag_edit(id=None):
    form = TagFrom()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash('标签已存在', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('标签修改成功', 'ok')
        redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


@admin.route('/movie/add/', methods=["GET", "POST"])
@admin_login
def movie_add():
    form = MoveForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


@admin.route('/movie/list/<int:page>/', methods=["GET"])
@admin_login
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)

#删除电影
@admin.route('/movie/del/<int:id>/', methods=["GET"])
@admin_login
def movie_del(id=None):
    movie=Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功', 'ok')
    return redirect(url_for('admin.movie_list',page=1))


@admin.route('/preview/add/')
@admin_login
def preview_add():
    return render_template('admin/preview_add.html')


@admin.route('/preview/list/')
@admin_login
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admin.route('/user/list/')
@admin_login
def user_list():
    return render_template('admin/user_list.html')


# 会员详情
@admin.route('/user/view/')
@admin_login
def user_view():
    return render_template('admin/user_view.html')


# 评论列表
@admin.route('/comment/list/')
@admin_login
def comment_list():
    return render_template('admin/comment_list.html')


# 电影收藏
@admin.route('/moviecol/list/')
@admin_login
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 操作日志
@admin.route('/oplog/list/')
@admin_login
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登录日志
@admin.route('/adminloginlog/list/')
@admin_login
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志
@admin.route('/userloginlog/list/')
@admin_login
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 权限添加
@admin.route('/auth/add/')
@admin_login
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin.route('/auth/list/')
@admin_login
def auth_list():
    return render_template('admin/auth_list.html')


# 角色添加
@admin.route('/role/add/')
@admin_login
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admin.route('/role/list/')
@admin_login
def role_list():
    return render_template('admin/role_list.html')


# 管理员添加
@admin.route('/admin/add/')
@admin_login
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin/list/')
@admin_login
def admin_list():
    return render_template('admin/admin_list.html')

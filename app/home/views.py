from . import home
from flask import render_template, redirect, url_for, flash, request, session
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PwdFrom
from werkzeug.security import generate_password_hash
from app.models import User, Usrelog,Preview
import uuid
from app import db, app
from werkzeug.utils import secure_filename
from functools import wraps
import os
import datetime


# 登录控制装饰器
def home_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# home 会员登录
@home.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash("密码错误！", "err")
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Usrelog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html', form=form)


# home 会员登出

@home.route('/logout/')
@home_login
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for("home.login"))


# home 会员注册
@home.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    return render_template('home/register.html', form=form)


# home 会员user
@home.route('/user/', methods=["GET", "POST"])
@home_login
def user():
    form = UserdetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data != "":
            file_face = secure_filename(form.face.data.filename)
            if not os.path.exists(app.config['FC_DIR']):
                os.makedirs(app.config['FC_DIR'])
                os.chmod(app.config['FC_DIR'], 'rw')
            user.face = change_filename(file_face)
            form.face.data.save(app.config['FC_DIR'] + user.face)

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash("昵称已经存在！", "err")
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash("邮箱已经存在！", "err")
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash("手机号已经存在！", "err")
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']

        db.session.add(user)
        db.session.commit()
        flash("修改成功！", "ok")
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


# home 找回密码
@home.route('/pwd/', methods=["GET", "POST"])
@home_login
def pwd():
    form = PwdFrom()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        user.pwd = generate_password_hash(data['new_pwd'])  # 加密修改admin.pwd

        db.session.add(user)
        db.session.commit()
        flash('密码修改成功,请重新登录', 'ok')

        return redirect(url_for('home.logout'))
    return render_template('home/pwd.html', form=form)


# home  评论
@home.route('/comments/')
@home_login
def comments():
    return render_template('home/comments.html')


# home 登录日志
@home.route('/loginlog/<int:page>/,methods=["GET]')
@home_login
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Usrelog.query.filter_by(
        user_id=int(session['user_id'])
    ).order_by(Usrelog.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# home 电影收藏
@home.route('/moviecol/')
@home_login
def moviecol():
    return render_template('home/moviecol.html')


# home index 首页
@home.route('/')
def index():
    return render_template('home/index.html')


# home index 上映预告
@home.route('/anmation/')
def anmation():
    data=Preview.query.all()
    print(data)
    return render_template('home/anmation.html',data=data)


# home index 首页搜索
@home.route('/search/')
def search():
    return render_template('home/search.html')


# home 播放
@home.route('/play/')
def play():
    return render_template('home/play.html')

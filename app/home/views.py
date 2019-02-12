from . import home
from flask import render_template, redirect, url_for,flash,request,session
from app.home.forms import RegistForm,LoginForm
from werkzeug.security import generate_password_hash
from app.models import User,Usrelog
import uuid
from app import db
from functools import wraps

# 访问控制装饰器
def home_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function



# home 会员登录
@home.route('/login/',methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        data=form.data
        user=User.query.filter_by(name=data['name']).first()
        print(user.name)
        if not user.check_pwd(data['pwd']):
            flash("密码错误！","err")
            return redirect(url_for('home.login'))
        session['user']=user.name
        session['user_id']=user.id
        userlog=Usrelog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html',form=form)


# home 会员登出

@home.route('/logout/')
@home_login
def logout():
    session.pop('user',None)
    session.pop('user_id',None)
    return redirect(url_for("home.login"))


# home 会员注册
@home.route('/register/',methods=["GET","POST"])
def register():
    form=RegistForm()
    if form.validate_on_submit():
        data=form.data
        user=User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功","ok")
    return render_template('home/register.html',form=form)


# home 会员user
@home.route('/user/')
@home_login
def user():
    return render_template('home/user.html')


# home 找回密码
@home.route('/pwd/')
@home_login
def pwd():
    return render_template('home/pwd.html')


# home  评论
@home.route('/comments/')
@home_login
def comments():
    return render_template('home/comments.html')


# home 登录日志
@home.route('/loginlog/')
@home_login
def loginlog():
    return render_template('home/loginlog.html')


# home 电影收藏
@home.route('/moviecol/')
@home_login
def moviecol():
    return render_template('home/moviecol.html')


# home index 首页
@home.route('/')
def index():
    return render_template('home/index.html')


# home index 电影列表
@home.route('/anmation/')
def anmation():
    return render_template('home/anmation.html')


# home index 首页搜索
@home.route('/search/')
def search():
    return render_template('home/search.html')


# home 播放
@home.route('/play/')
def play():
    return render_template('home/play.html')




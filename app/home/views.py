from . import home
from flask import render_template, redirect, url_for


# home 首页
@home.route('/')
def index():
    return render_template('home/index.html')


# home 会员登录
@home.route('/login/')
def login():
    return render_template('home/login.html')


# home 会员登出

@home.route('/logout/')
def logout():
    return redirect(url_for("home.login"))


# home 会员注册
@home.route('/register/')
def register():
    return render_template('home/register.html')


# home 会员user
@home.route('/user/')
def user():
    return render_template('home/user.html')


# home 找回密码
@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')


# home  评论
@home.route('/comments/')
def comments():
    return render_template('home/comments.html')



# home 登录日志
@home.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')


# home 电影收藏
@home.route('/moviecol/')
def moviecol():
    return render_template('home/moviecol.html')


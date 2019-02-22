# ！/user/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/movie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '7e020166dc284ad187e32cbda0a9d4ac'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/" )
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/users/" )

app.debug = False
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


# 404
@app.errorhandler(404)
def page_not_fount(error):
    return render_template('home/404.html'), 404

# ！/user/bin/python3
# -*- coding:utf-8 -*-

from datetime import datetime
from app import db
from werkzeug.security import check_password_hash


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=False)
    phone = db.Column(db.String(11), unique=False)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=False)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=False)  # 唯一标识符

    userlogs = db.relationship("Usrelog", backref="user")  # 会员日志外键关联userlog表
    comments = db.relationship("Comment", backref="user")  # 评论关联comment表
    moviecols = db.relationship("Moviecol", backref="user")  # 收藏关联moviecol表

    def __repr__(self):
        return "<User %r>" % self.name


# 会员日志
class Usrelog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属会员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "Userlog %r" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Movie", backref="tag")  # 电影　外键关联

    def __repr__(self):
        return "Tag %r" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级　
    playnum = db.Column(db.BigInteger)  # 播放量　
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))  # 所属标签　
    area = db.Column(db.String(255))  # 上映地区　
    release_time = db.Column(db.Date)  # 上映时间　
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    comments = db.relationship("Comment", backref="movie")  # 评论关联comment表
    moviecols = db.relationship("Moviecol", backref="movie")  # 收藏关联moviecol表

    def __repr__(self):
        return "Movie %r" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "Preview %r" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # 所属电影　
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "Comment %r" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # 所属电影　
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "Moviecol %r" % self.id


# 权限数据
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色数据模型
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    authos = db.Column(db.String(600))  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return "Role %r" % self.name


# 管理员角色模型
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0 表示超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    adminlogs = db.relationship('AdminLog', backref='admin')
    oplogs = db.relationship('OpLog', backref='admin')

    def __repr__(self):
        return "Admin %r" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志模型
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "AdminLog %r" % self.id


if __name__ == "__main__":
    db.create_all()


# 操作日志模型
class OpLog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "OpLog %r" % self.id


if __name__ == "__main__":
    #db.create_all()

    # role=Role(
    #     name='超级管理员',
    #     authos=''
    # )
    # db.session.add(role)
    # db.session.commit()

    from werkzeug.security import generate_password_hash #密码hash加密
    admin=Admin(
        name='movie',
        pwd=generate_password_hash('movie'),
        is_super=0,
        role_id=1,
    )

    db.session.add(admin)
    db.session.commit()

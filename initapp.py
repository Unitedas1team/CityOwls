import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import logging
import cv2

bootstrap = Bootstrap()
db = SQLAlchemy()   #创建数据库操作对象
login_manager = LoginManager()  #初始化log函数  保存登录设置
csrf = CSRFProtect()
login_manager.login_view = 'patrol'
camera = cv2.VideoCapture(0)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'dev key')  #找到文件夹
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    basedir = os.path.abspath(os.path.dirname(__file__))  #ab获取（）内文件完整路径  di去掉文件名返回目录
    prefix = 'sqlite:////'      #数据库uri格式  内存型
    app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(basedir, 'data-dev.db')
    app.config["STORE_PATH"] = os.path.join(basedir, 'store')
    app.config["IMG_PATH"] = os.path.join(basedir,'static','images')
    app.config["VIDEO_PATH"] = os.path.join(basedir,'static','raws',)

    app.logger.setLevel(logging.INFO)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user
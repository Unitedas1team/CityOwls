import click
from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from initapp import create_app, db
from models import Admin,Weather,Devices,Checkin,Inspection,Repair,Light
from pathlib import Path
import os
import shutil

app = create_app()


@app.shell_context_processor  # 自动导入数据库
def make_shell_context():
    return dict(db=db, Admin=Admin,Weather=Weather,Devices=Devices,Checkin=Checkin,Inspection=Inspection,Repair=Repair,Light=Light)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database.初始化数据库"""
    if drop:  # 判断是否输出选项
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()  # 从新生成表  删除表
        click.echo('Drop tables.')  # 输出提示信息
        dirlist = os.listdir(current_app.config['STORE_PATH'])
        for i in dirlist:
            shutil.rmtree(Path(current_app.config['STORE_PATH']) / i)
    db.create_all()  # 从新创建表
    click.echo('Initialized database.')


@app.cli.command()
def init():
    """Initialize Albumy."""
    click.echo('Initializing the database...')
    db.create_all()
    click.echo('Done.')


import views

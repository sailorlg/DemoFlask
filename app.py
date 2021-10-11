
import os
from jinja2.utils import generate_lorem_ipsum, escape
from flask import Flask, url_for, request, redirect, make_response, json, jsonify, session, abort, g, \
    render_template, Markup, flash, send_from_directory
from urllib.parse import urlparse, urljoin
# Chapter: 4.4.4_4
from flask_wtf.csrf import validate_csrf  # 验证CSRF令牌
from wtforms import ValidationError

from flask_ckeditor import CKEditor  # 传入CDEditor, Chapter 4.4.5

import click
import uuid

# 导入SQLAlchemy包, Chapter 5.3
from flask_sqlalchemy import SQLAlchemy

from ConfigDemo import ConfigDemo


from flask_migrate import Migrate

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量
ckeditor = CKEditor(app)  # 实例化Flask-CKEditor提供的CKEditor类

# 实例化Flask-SQLAlchemy提供的SQLAlchemy类, 传入程序实例,已完成扩展的初始化
# Chapter 5.3
db = SQLAlchemy(app)

# 实例化Migrate类
# Chapter 5.6.2
migrate = Migrate(app, db)


@app.cli.command()
def initdb():
    """
    Function:创建数据库和表的flask命令
    :return:
    """
    db.create_all()
    click.echo("Initialized database.")


# @app.shell_context_processor
# def make_shell_context():
#     """
#     Function: 为了在flask shell中, 不必import也能用python对象, 把需要的对象注册到上下文环境中
#     Chapter: 5.5.1
#     :return:
#     """
#     v_dict = dict(db=db)
#     return v_dict







#######################################################################################################




@app.route("/")
def index_view():
    """
    Function: 演示从页面读入提交的数据并保存到数据库的过程
              这是首页面, 添加链接能跳转到写笔记页面
    Chapter: 5.4.2_1~2
    :return:
    """
    print("app.py => index_view => db : ", db)
    return render_template("index.html")


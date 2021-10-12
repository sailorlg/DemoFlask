
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

# 发送邮件的表单
# Chapter 6.1.3
from form.forms import SendMailForm

from flask_migrate import Migrate

# 导入Flask-Mail包, Flask-Mail包装了Python标准库中的smtplib包, 简化了在Flask中发送电子邮件的过程
from flask_mail import Mail, Message

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量
ckeditor = CKEditor(app)  # 实例化Flask-CKEditor提供的CKEditor类

# 实例化Flask-SQLAlchemy提供的SQLAlchemy类, 传入程序实例,已完成扩展的初始化
# Chapter 5.3
db = SQLAlchemy(app)

# 实例化Migrate类
# Chapter 5.6.2
migrate = Migrate(app, db)

# 实例化Flask-Mail提供的Mail类并传入程序实例以完成初始化
mail = Mail(app)

################################################################################

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
    # send_mail(None, None, None)
    print("app.py => index_view => db : ", db)
    return render_template("index.html")


def send_mail(subject, to, body):
    """
    Function:发送邮件
    :param subject:
    :param to:
    :param body:
    :return:
    Chapter: 6.1.3, 6.3.2
    """
    if subject is None:
        mail_subject = 'Test'
    else:
        mail_subject = subject

    if to is None:
        mail_to = ['guanghai.li@samsungimc.com']  # 这里需要用列表类型.
    else:
        mail_to = to

    if body is None:
        mail_body = 'TEST From Flask Demo'
    else:
        mail_body = body

    print("app.py => send_mail => mail_to : ", mail_to)
    mail_message = Message(mail_subject, mail_to, mail_body)
    mail_message.html = render_template('email/emailbase.html', name=mail_subject, content=mail_body)
    mail.send(mail_message)


@app.route("/sendmail", methods=['GET', 'POST'])
def send_mail_page():
    """
    Function:发送邮件
    :return:
    """
    form = SendMailForm()

    if form.validate_on_submit():
        print("app.py => send_mail_page => form.address.data : ", form.address.data)
        mail_address = []
        mail_address.append(str(form.address.data))
        print("app.py => send_mail_page => mail_address : ", mail_address)

        mail_subject = form.mail_title.data
        mail_content = form.mail_body.data

        send_mail(mail_subject, mail_address, mail_content)
        flash("Mail sent successfully!")
        return redirect(url_for("index_view"))  # 返回到首页

    return render_template("sendmail.html", form=form)

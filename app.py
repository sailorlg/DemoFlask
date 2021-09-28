
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
from form.forms import NewNoteListForm

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量
ckeditor = CKEditor(app)  # 实例化Flask-CKEditor提供的CKEditor类

# 实例化Flask-SQLAlchemy提供的SQLAlchemy类, 传入程序实例,已完成扩展的初始化
# Chapter 5.3
db = SQLAlchemy(app)


@app.cli.command()
def initdb():
    """
    Function:创建数据库和表的flask命令
    :return:
    """
    db.create_all()
    click.echo("Initialized database.")


class NoteList(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.3.2
    """
    note_id = db.Column(db.Integer, primary_key=True)
    note_body = db.Column(db.Text)




#######################################################################################################




@app.route("/")
def index_view():
    """
    Function: 演示从页面读入提交的数据并保存到数据库的过程
              这是首页面, 添加链接能跳转到写笔记页面
    Chapter: 5.4.2_1
    :return:
    """
    print("app.py => index_view => db : ", db)
    return render_template("index.html")

@app.route("/writenote", methods=['GET', 'POST'])
def write_note():
    """
    Function: 演示从页面读入提交的数据并保存到数据库的过程
              创建显示和处理写笔记页面的视图
    :return:
    """
    form = NewNoteListForm()
    if form.validate_on_submit():  # 处理提交后的内容
        notebody = form.notebody.data
        print("app.py => write_note => notebody : ", notebody)
        a_note = NoteList(note_body=notebody)
        db.session.add(a_note)
        db.session.commit()
        flash("Saved Successfully!")
        return redirect(url_for("index_view"))
    return render_template("write_note.html", form=form)


@app.route("/readnote", methods=['GET', 'POST'])
def read_note():
    """
    Function: 显示从数据库读取笔记的内容后显示在页面
    :return:
    """
    notes = NoteList.query.all()
    return render_template("read_note.html", notes=notes)


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
from form.forms import NewNoteListForm, EditNoteForm, DeleteNoteForm

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


@app.shell_context_processor
def make_shell_context():
    """
    Function: 为了在flask shell中, 不必import也能用python对象, 把需要的对象注册到上下文环境中
    Chapter: 5.5.1
    :return:
    """
    v_dict = dict(db=db, NoteList=NoteList, AuthorList=AuthorList,
                  ArticleList=ArticleList, Book=Book, Writer=Writer, Singer=Singer, Song=Song,
                  Citizen=Citizen, City=City, Country=Country, Capital=Capital, Student=Student,
                  Teacher=Teacher, Post=Post, Comment=Comment, Draft=Draft)
    return v_dict


class NoteList(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.3.2
    """
    note_id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(100))
    note_body = db.Column(db.Text)


class AuthorList(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('ArticleList')


class ArticleList(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author_list.id'))


class Writer(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', back_populates='writer')


class Book(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    writer = db.relationship('Writer', back_populates='books')


class Singer(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship('Song', backref='singer')

class Song(db.Model):
    """
    Function: 定义一个数据库表模型
    Chapter: 5.5.2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    singer_id = db.Column(db.Integer, db.ForeignKey("singer.id"))


class Citizen(db.Model):
    """
    Function: 定义一个多对一关系的模型,
              市民, "多"的一侧
    Chapter: 5.5.3
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))  # 创建外键
    city = db.relationship('City')  # 定义关系属性, 获取城市对象


class City(db.Model):
    """
    Function: 定义多对一关系的模型
              城市, "一"的一侧
    Chapter: 5.5.3
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)


class Country(db.Model):
    """
    Function: 定义一对一模型
    Chapter: 5.5.4
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    capital = db.relationship('Capital', back_populates='country', uselist=False)


class Capital(db.Model):
    """
    Function: 定义一对一关系
    Chapter: 5.5.4
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', back_populates='capital')


# Student和Teacher的关系表
# Chapter: 5.5.5
association_table = db.Table('association', db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    """
    Function: 定义多对多关系
    Chapter: 5.5.5
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher', secondary=association_table, back_populates='students')


class Teacher(db.Model):
    """
    Function: 定义多对多关系
    Chapter: 5.5.5
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student', secondary=association_table, back_populates='teachers')


class Post(db.Model):
    """
    Function:演示数据库的级联操作
             存储文章(帖子)的模型
    Chapter: 5.7.1
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    comments = db.relationship('Comment', back_populates='post', cascade='save-update, merge, delete')


class Comment(db.Model):
    """
    Function:演示数据库的级联操作
             存储评论的模型
    Chapter: 5.7.1
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


class Draft(db.Model):
    """
    Function:演示事件监听
    Chapter: 5.7.2
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)





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


@app.route("/writenote", methods=['GET', 'POST'])
def write_note():
    """
    Function: 演示从页面读入提交的数据并保存到数据库的过程
              创建显示和处理写笔记页面的视图
    Chapter: 5.4.2_1~2
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
    Chapter: 5.4.2_1~2
    :return:
    """
    notes = NoteList.query.all()
    deleteform = DeleteNoteForm()
    # return render_template("read_note.html", notes=notes)  # 在写Chapter 5.4.2_4, 删除功能演示的时候, 修改为下面的代码
    return render_template("read_note.html", notes=notes, form=deleteform)


@app.route("/editnote/<int:note_id>", methods=['GET', 'POST'])
def edit_note(note_id):
    """
    Function:演示修改一个已经显示在页面中的数据
    Chapter: 5.4.2_3
    :param note_id:
    :return:
    """
    form = EditNoteForm()
    note = NoteList.query.get(note_id)

    if form.validate_on_submit():
         note.note_body = form.notebody.data
         db.session.commit()
         flash("Your note is updated!")
         return redirect(url_for("read_note"))

    form.notebody.data = note.note_body
    return render_template("edit_note.html", form=form)


@app.route("/deletenote/<int:note_id>", methods=['POST'])
def delete_note(note_id):
    """
    Function:演示修改一个已经显示在页面中的数据
    Chapter: 5.4.2_4
    :param note_id:
    :return:
    """
    form = DeleteNoteForm()
    if form.validate_on_submit():
        print("app.py => delete_note : running......")
        note = NoteList.query.get(note_id)  # 获取对应的记录
        db.session.delete(note)  # 删除记录
        db.session.commit()  # 提交修改
        flash("Your note is deleted!")
    else:
        abort(400)
    return redirect(url_for("read_note"))


# @db.event.listens_for(Draft.body, 'set')
# def increment_edit_time(target, value, oldvalue, initiator):
#     """
#     Function:在listens_for装饰器分别传入Draft.body和set作为target和identifier参数的值
#              监听函数接受所有set()事件方法接收的参数, 其中的targete参数表示触发时间的模型类实例,
#              使用target.edit_time即可获取我们需要叠加的字段.
#              其他的参数也需要照常写出, 虽然这里没有用到.
#     :param target:
#     :param value: 被设置的值
#     :param oldvalue: 被取代的旧值
#     :param initiator:
#     :return:
#     Chapter: 5.7.2_1
#     """
#     if target.edit_time is not None:
#         target.edit_time += 1


@db.event.listens_for(Draft.body, 'set', named=True)
def increament_edit_time(**kwargs):
    """
    Function: 需要现在装饰器中把参数name设置为True, 可以在监听函数中接收**kwargs作为参数.
              然后在函数中可以使用参数名作为键来从kwargs字典获取对应的参数值.
    :param kwargs:
    :return:
    Chapter: 5.7.2_2
    """
    if kwargs['target'].edit_time is not None:
        kwargs['target'].edit_time += 1
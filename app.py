
import os

from flask import Flask, url_for, request, redirect, make_response, json, jsonify, session, abort
import click

from ConfigDemo import ConfigDemo

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量


@app.route("/")
def index():
    return "<H1>Hello, World!</H1>"

@app.route("/hi", methods=['GET', 'POST'])
@app.route("/hello", methods=['GET', 'POST'])
def say_hello():
    """
    Function:获取从浏览器传过来的参数name的值, 并显示
             从cookie中获取值
             从session中取值
    :return:
    """
    print(request)
    print(request.args)

    # v_name = request.args.get('name')
    # if v_name is None:  # 如果浏览器没有数据name的值
    #     v_name = "Nobody"
    # v_name = request.args.get('name', 'Nobody')  # 等价于上面的代码

    v_name = request.args.get('name')  # 从浏览器的URL中获取name值
    if v_name is None:
        v_name = request.cookies.get('name', 'COOKIE')

    response =  "<H1>Say Hello to {}!</H1>".format(v_name)

    # 根据用户认证状态返回不同的值
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += "UN-Authenticated"
    return response

@app.route("/greet/", defaults={"name": "Programmer"})
@app.route("/greet/<name>")
def greet(name):
    return "<H1>Welcome, %s!</H1>" % name

@app.route("/demoname")
def demoname():
    v_demo_name = app.config['DEMO_NAME']
    return "<H1>I am {0}!</H1>".format(v_demo_name)

@app.route("/geturl")
def geturl():
    """
    Function:测试url_for()函数
    :return:
    """
    v_url = url_for("greet")
    v_url_external = url_for("greet", _external=True)
    return ("Greet's internal URL is {0}, external URL is {1}.".format(v_url, v_url_external))

@app.cli.command()
def get_demo_name():
    """
    Function: 测试Flask CLI命令的功能
    在进入虚拟环境的命令行中输入"flask get-demo-name"可执行该命令
    :return:
    """
    v_demo_name = app.config['DEMO_NAME']
    click.echo(v_demo_name)

@app.route("/goback/<int:year>")
def go_back(year):
    v_now = year
    v_atfer_year = 2021 + year
    return "Welcome to atfer %d years, Now is %d." % (v_now, v_atfer_year)

colors = ['blue', 'white', 'red']
@app.route("/color/<any(%s):color>"%str(colors)[1:-1])
def any_colors(color):
    return "<H1><font color=%s>Welcome</font></H1>"%color

@app.route("/redirect")
def redirect_goto():
    """
    Function:测试重定向功能
    :return:
    """
    print("app.py => redirect_to ")

    # 方法1
    # return "", 302, {"Location": "HTTP://www.imarketchina.net"}

    # 方法2
    # return redirect("http://bbs.fengniao.com")

    # 方法3
    return redirect(url_for("say_hello"))

@app.route("/contenttype/<type>")
def return_requested_type(type):
    """
    Function:相应格式测试
             测试cookie
    :param type:
    :return:
    """

    if type.upper() == "JSON":
        # 方法1
        # v_data = {"name":"ZhangSan",
        #           "Job": "Student"}
        # response = make_response(json.dumps(v_data))
        # response.mimetype = "application/json"
        # return response
        v_data = {"name":"ZhangSan",
                  "Job": "Student"}
        response = jsonify(v_data)
    elif type.upper() == "HTML":
        v_data = "<!DOCTYPE html>" \
                 "<html>" \
                 "<head></head>" \
                 "<body>" \
                 "    <H1>Note</H1>" \
                 "    <p>To: Jane</p>" \
                 "    <p><font color=red>Content: I LOVE YOU</font></p>" \
                 "</body>" \
                 "</html>"
        response = make_response(v_data)
        response.mimetype = "text/html"

    else:
        response = jsonify(message="HTML or JSON"), 500

    response.set_cookie('name', type)

    return response

@app.route("/set/<name>")
def set_cookie(name):
    response = make_response(redirect(url_for("say_hello")))
    response.set_cookie("name", name)
    return response

@app.route("/login")
def login():
    """
    Function: 设置session
    :return:
    """
    session['logged_in'] = True  # 写入session
    return redirect(url_for('say_hello'))


@app.route("/admin")
def admin():
    if 'logged_in' not in session:
        abort("403")
    return "<H1>WELCOME</H1>"

@app.route("/logout")
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('say_hello'))
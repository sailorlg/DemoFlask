#
# import os
#
# from flask import Flask, url_for, request, redirect, make_response, json, jsonify, session, abort, g
# from urllib.parse import urlparse, urljoin
# import click
#
# from ConfigDemo import ConfigDemo
#
# app = Flask(__name__)  # 创建FlaskApp
# app = ConfigDemo(app).app  # 读入全局配置变量
#
#
# @app.route("/")
# def index():
#     return "<H1>Hello, World!</H1>"
#
# @app.route("/hi", methods=['GET', 'POST'])
# @app.route("/hello", methods=['GET', 'POST'])
# def say_hello():
#     """
#     Function:获取从浏览器传过来的参数name的值, 并显示
#              从cookie中获取值
#              从session中取值
#     :return:
#     """
#     print(request)
#     print(request.args)
#
#     # v_name = request.args.get('name')
#     # if v_name is None:  # 如果浏览器没有数据name的值
#     #     v_name = "Nobody"
#     # v_name = request.args.get('name', 'Nobody')  # 等价于上面的代码
#
#     v_name = request.args.get('name')  # 从浏览器的URL中获取name值
#     if v_name is None:
#         v_name = request.cookies.get('name', 'COOKIE')
#
#     response =  "<H1>Say Hello to {}!</H1>".format(v_name)
#
#     # 根据用户认证状态返回不同的值
#     if 'logged_in' in session:
#         response += '[Authenticated]'
#     else:
#         response += "UN-Authenticated"
#     return response
#
# @app.route("/greet/", defaults={"name": "Programmer"})
# @app.route("/greet/<name>")
# def greet(name):
#     return "<H1>Welcome, %s!</H1>" % name
#
# @app.route("/demoname")
# def demoname():
#     v_demo_name = app.config['DEMO_NAME']
#     return "<H1>I am {0}!</H1>".format(v_demo_name)
#
# @app.route("/geturl")
# def geturl():
#     """
#     Function:测试url_for()函数
#     :return:
#     """
#     v_url = url_for("greet")
#     v_url_external = url_for("greet", _external=True)
#     return ("Greet's internal URL is {0}, external URL is {1}.".format(v_url, v_url_external))
#
# @app.cli.command()
# def get_demo_name():
#     """
#     Function: 测试Flask CLI命令的功能
#     在进入虚拟环境的命令行中输入"flask get-demo-name"可执行该命令
#     :return:
#     """
#     v_demo_name = app.config['DEMO_NAME']
#     click.echo(v_demo_name)
#
# @app.route("/goback/<int:year>")
# def go_back(year):
#     v_now = year
#     v_atfer_year = 2021 + year
#     return "Welcome to atfer %d years, Now is %d." % (v_now, v_atfer_year)
#
# colors = ['blue', 'white', 'red']
# @app.route("/color/<any(%s):color>"%str(colors)[1:-1])
# def any_colors(color):
#     return "<H1><font color=%s>Welcome</font></H1>"%color
#
# @app.route("/redirect")
# def redirect_goto():
#     """
#     Function:测试重定向功能
#     :return:
#     """
#     print("app.py => redirect_to ")
#
#     # 方法1
#     # return "", 302, {"Location": "HTTP://www.imarketchina.net"}
#
#     # 方法2
#     return redirect("http://bbs.fengniao.com")
#
#     # 方法3
#     # return redirect(url_for("say_hello"))
#
# @app.route("/contenttype/<type>")
# def return_requested_type(type):
#     """
#     Function:相应格式测试
#              测试cookie
#     :param type:
#     :return:
#     """
#
#     if type.upper() == "JSON":
#         # 方法1
#         # v_data = {"name":"ZhangSan",
#         #           "Job": "Student"}
#         # response = make_response(json.dumps(v_data))
#         # response.mimetype = "application/json"
#         # return response
#         v_data = {"name":"ZhangSan",
#                   "Job": "Student"}
#         response = jsonify(v_data)
#     elif type.upper() == "HTML":
#         v_data = "<!DOCTYPE html>" \
#                  "<html>" \
#                  "<head></head>" \
#                  "<body>" \
#                  "    <H1>Note</H1>" \
#                  "    <p>To: Jane</p>" \
#                  "    <p><font color=red>Content: I LOVE YOU</font></p>" \
#                  "</body>" \
#                  "</html>"
#         response = make_response(v_data)
#         response.mimetype = "text/html"
#
#     else:
#         response = jsonify(message="HTML or JSON"), 500
#
#     response.set_cookie('name', type)
#
#     return response
#
# @app.route("/set/<name>")
# def set_cookie(name):
#     response = make_response(redirect(url_for("say_hello")))
#     response.set_cookie("name", name)
#     return response
#
# @app.route("/login")
# def login():
#     """
#     Function: 设置session
#     :return:
#     """
#     session['logged_in'] = True  # 写入session
#     return redirect(url_for('say_hello'))
#
#
# @app.route("/admin")
# def admin():
#     if 'logged_in' not in session:
#         abort("403")
#     return "<H1>WELCOME</H1>"
#
# @app.route("/logout")
# def logout():
#     if 'logged_in' in session:
#         session.pop('logged_in')
#     return redirect(url_for('say_hello'))
#
# @app.route("/goods")
# def goods_page():
#     return "<H1>Goods Page</H1><a href='%s'> Do Something</a>" % \
#            url_for('do_something', next=request.full_path)
#
# @app.route("/oders")
# def orders_page():
#     return "<H1>Orders Page</H1><a href='%s'> Do Something</a>" % \
#            url_for('do_something', next=request.full_path)
#
# @app.route("/do-something")
# def do_something():
#     """
#     Function:测试重定向功能
#     :return:
#     """
#     # return redirect(url_for("say_hello"))
#     print("Now, going back - step 01")
#     return redirect_goback()
#
# def redirect_goback(default_page='demoname', **kwargs):
#     print("Now, going back - step 02")
#     for target in request.args.get("next"), request.referrer:
#         print("redirect_goback => ", target)
#         if not target:
#             print("redirect_goback => continue")
#             continue
#         if is_safe_url(target):
#             return redirect(target)
#     return redirect(url_for(default_page, **kwargs))
#
# @app.route("/logout")
# def log_out_function():
#     """
#     Function: 测试退出功能
#     :return:
#     """
#     if "logged_in" in session:
#         session.pop("logged_in")
#     return redirect(url_for("say_hello"))
#
# @app.before_request
# def get_name():
#     g.name = request.args.get('name')
#     print(g.name)
#
# def is_safe_url(target):
#     """
#     Function: 判断跳转的目标URL是不是安全的.
#     :param target:
#     :return:
#     """
#     print("is_safe_url => target : ", target)
#     rer_url = urlparse(request.host_url)
#     print("is_safe_url => rer_url : ", rer_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     print("is_safe_url => test_url: ", test_url)
#     return test_url.scheme in ("http", "https") and rer_url.netloc == test_url.netloc

import os
from jinja2.utils import generate_lorem_ipsum, escape
from flask import Flask, url_for, request, redirect, make_response, json, jsonify, session, abort, g, \
    render_template, Markup, flash
from urllib.parse import urlparse, urljoin
import click

from form.forms import LoginForm  # 导入form文件夹下form.py文件的LoginForm类
from ConfigDemo import ConfigDemo

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量

@app.route("/post")
def show_post():
    """
    Function: 演示通过Ajax的部分加载
    :return:
    """
    v_post_body = generate_lorem_ipsum(n=2)  # 随机生成2段文本
    return """
        <H1>A very log post</H1>
        <div class="body">%s</div>
        <button id="load">Load More ...</button>
        <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
        <script type="text/javascript">
            $(function() {
                $('#load').click(function() {
                    $.ajax({
                        url:'/more',  // 目标URL
                        type: 'get',  // 请求方法
                        success: function(data){  // 返回2**相应后触发的回调函数
                            $('.body').append(data);  // 将返回的响应写入页面中
                        }
                    })
                })
            })
        </script>
    """ % v_post_body


@app.route("/more")
def load_post():
    """
    Function: 在show_post()方法部分加载时, 提供需要加载的内容
    :return:
    """
    print("load_post => is running......")
    return generate_lorem_ipsum(n=1)


@app.route("/hello")
def hello_function():
    """
    Function: 演示对输入进行转义清洗的功能
    :return:
    """
    v_name = request.args.get('name', 'My Owner')

    # return '<H1>Hello, %s!</H1>' % v_name  # 没有清洗的功能
    return '<H1>Hello, %s!</H1>' % escape(v_name)  # 通过escape进行清洗


@app.route("/watchlist")
def f_watchlist():
    """
    Function: 演示模板的使用
    :return:
    """
    v_user = {"username": "ZhangSan",
            "bio": "A boy only"}
    v_movies = [
        {"name": "My Neighbor Totoro", "year": "1988"},
        {"name": "Three Colors Trilogy", "year": "1993"},
        {"name": "Perfect Blue", "year": "1997"},
        {"name": "The Bucket List", "year": "2007"},
        {"name": "CoCo", "year": "2017"},
    ]
    return render_template('watchlist.html', user=v_user, movies=v_movies)


@app.route("/")
def index_view():
    """

    :return:
    """
    return render_template('index.html', foo="ImFoo", name="baz")


@app.template_filter()
def musicals(s):
    """
    Function: 注册自定义的过滤器
              在给定字符串后面加上音乐符号
    :param s:
    :return:
    """
    return s + Markup('&#9835;')


@app.template_global()
def bar():
    """
    Function: 注册全局对象
              返回字符串
    :return:
    """
    return "I am bar() function."


@app.template_test()
def baz(n):
    """
    Function: 注册自定义测试器
    :param n:
    :return:
    """
    if n == "baz":
        return True
    return False


@app.route("/flash")
def display_flash():
    """
    Function: 设置flash内容后, 跳转到索引页面
              在索引页面中读取flash内容后显示
    :return:
    """
    flash("I am flash, Only Flash!")
    flash("Second Flash!")
    return redirect(url_for("index_view"))


@app.errorhandler(404)
def page_not_found (e):
    return render_template('errors/404.html'), 404


@app.route("/basic")
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)
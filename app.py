
from flask import Flask, url_for, request
import click

from ConfigDemo import ConfigDemo

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量

@app.route("/")
def index():
    return "<H1>Hello, World!</H1>"

@app.route("/hi")
@app.route("/hello")
def say_hello():
    """
    Function:获取从浏览器传过来的参数name的值, 并显示
    :return:
    """
    print(request)
    print(request.args)

    v_name = request.args.get('name')
    if v_name is None:  # 如果浏览器没有数据name的值
        v_name = "Nobody"

    return "<H1>Say Hello to {}!</H1>".format(v_name)

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
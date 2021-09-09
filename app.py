
from flask import Flask

from ConfigDemo import ConfigDemo

app = Flask(__name__)  # 创建FlaskApp
app = ConfigDemo(app).app  # 读入全局配置变量

@app.route("/")
def index():
    return "<H1>Hello, World!</H1>"

@app.route("/hi")
@app.route("/hello")
def say_hello():
    return "<H1>Say Hello!</H1>"

@app.route("/greet/", defaults={"name": "Programmer"})
@app.route("/greet/<name>")
def greet(name):
    return "<H1>Welcome, %s!</H1>" % name

@app.route("/demoname")
def demoname():
    v_demo_name = app.config['DEMO_NAME']
    return "<H1>I am {0}!</H1>".format(v_demo_name)
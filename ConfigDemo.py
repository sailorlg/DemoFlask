
import os

from flask import Flask
from flask_wtf import FlaskForm

class ConfigDemo():
    """这个类是用于配置Flask的全局变量"""
    def __init__(self, p_app):
        self.app = p_app
        self.private_setting = {}
        self.read_private_keys()
        self.set_config()

    def set_config(self):
        """
        Function:设施配置变量, 这里的配置变量是在程序开发的时候确定了的
        :return:
        """
        self.app.config['DEMO_NAME'] = "FlaskDemo"
        self.app.secret_key = os.getenv('SECURITY_KEY')

        # 把WTF_I18N_ENABLED设置为False, 会让Flask-WTF使用内置的错误消息翻译
        self.app.config['WTF_I18N_ENABLED'] = False

        # 上传图片文件后保存的路径
        self.app.config['UPLOAD_PATH'] = os.path.join(self.app.root_path, 'uploadedimages')

        # 设置允许上传的文件类型的扩展名, Chapter: 4.4.4_4
        self.app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

        # 配置数据库URI
        # Chapter 5.3.1
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 'sqlite:///' + os.path.join(self.app.root_path, 'db', 'c6demosqlite3.db'))

        # 修补在进行flask命令时出现FSADeprecationWarning的问题
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # 设置邮件服务器配置
        # Chapter 6.1.1
        self.app.config['MAIL_SERVER'] = 'smtp.163.com'  # 发件服务器地址
        self.app.config['MAIL_USERNAME'] = 'sailorlg@163.com'  # 发信服务器的用户名
        self.app.config['MAIL_PASSWORD'] = self.private_setting['MAIL']
        self.app.config['MAIL_DEFAULT_SENDER'] = ('sailorlg', 'sailorlg@163.com')


    def read_private_keys(self):
        """
        Function:读取私密内容
        :return:
        Chapter: 6.1.1
        """
        with open('cenv/settings') as a_file:
            self.private_setting['MAIL'] = a_file.read()

        print("ConfigDemo.py => ConfigDemo => read_private_keys : self.private_setting['MAIL'] : ",
              self.private_setting['MAIL'])
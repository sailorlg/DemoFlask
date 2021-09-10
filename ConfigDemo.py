
import os

from flask import Flask

class ConfigDemo():
    """这个类是用于配置Flask的全局变量"""
    def __init__(self, p_app):
        self.app = p_app
        self.set_config()

    def set_config(self):
        """
        Function:设施配置变量, 这里的配置变量是在程序开发的时候确定了的
        :return:
        """
        self.app.config['DEMO_NAME'] = "FlaskDemo"
        self.app.secret_key = os.getenv('SECURITY_KEY')





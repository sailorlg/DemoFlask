from flask_wtf import FlaskForm

# 4.4.4_1~3
# 为了文件上传我们使用扩展Flask-WTF提供的FileField类, 他继承自WTForms提供的上传字段FileField, 添加了Flask的继承
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, \
    MultipleFileField,TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

# 从flask-ckeditor包导入
# Chapter: 4.4.5
from flask_ckeditor import CKEditorField

class MyBaseForm(FlaskForm):
    class Meta:
        """
        Function:在自定义基类中定义Meta类, 并在locals列表中加入简体中文的地区字符串.
                 基类是继承FlaskForm的
        Chapter: 4.4.1
        """
        locals = ['zh']


class SendMailForm(MyBaseForm):
    """
    Function: 创建发送邮件的页面
              用于构建表单
    Chapter: 6.1.3
    """
    address = StringField(label="Send mail to", validators=[DataRequired()])
    mail_title = StringField(label='Mail subject', validators=[DataRequired()])
    mail_body = StringField(label="Mail Content", validators=[DataRequired()])
    submit = SubmitField("SendMail")
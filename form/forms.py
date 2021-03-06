from flask_wtf import FlaskForm

# 4.4.4_1~3
# 为了文件上传我们使用扩展Flask-WTF提供的FileField类, 他继承自WTForms提供的上传字段FileField, 添加了Flask的继承
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField
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


# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
#     remember = BooleanField("Remember me")
#     submit = SubmitField("Login")

class LoginForm(MyBaseForm):
    """
    Function:继承MyBaseForm将错误消息语言设置为中文
    Chapter: 4.4.1
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class AskAgeForm(MyBaseForm):
    """
    Function: 演示自定义验证器
    Chapter: 4.4.3_1
    """
    answer = IntegerField("Input your age:")
    submit = SubmitField("提交")

    def validate_answer(form, field):
        """
        Function:如果输入的数字大于200, 则提示"请输入正确的数字"
                 这个行内验证器需要把数据提交到服务器段后才验证?
        :param field:
        :return:
        """
        # print("forms.py => AskAgeForm => validate_answer : running ")
        if field.data > 200:
            raise ValidationError("Data Error")


def check_name(message=None):
    """
    Function:自定义验证器中的全局验证器的用法, 自定义全局验证器
    Chapter: 4.4.3_2
    """
    if message == None:
        message = "Only alphabet can be used!"

    def _check_name(form, field):
        """
        Function: 判断是否为纯字母组成的字符串
        :param form:
        :param field:
        :return:
        """
        v_data = field.data
        for a_character in v_data:
            if a_character.isalpha():
                v_data = v_data.replace(a_character, "")  # 若为字母，使用空格代替
        v_len = v_data.split()
        if len(v_len) > 0:
            raise ValidationError(message)
    return _check_name


class AskNameForm(MyBaseForm):
    """
    Function:自定义验证器中的全局验证器的用法
    Chapter: 4.4.3_2
    """
    name = StringField("Username", validators=[check_name()])
    submit = SubmitField("PutMyName")


class UploadSingleImageForm(FlaskForm):
    """
    Function: 演示上传单个图片文件
    Chapter: 4.4.4_1~3
    """
    description = StringField("Introduce")
    image = FileField("Upload Beautify",
                      validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField("GO")


class UploadMultiImageForm(MyBaseForm):
    """
    Function:演示上传多个图片文件
             富文本编辑功能增加
             单个页面多个表单的演示
    Chapter: 4.4.4_4, 4.4.5, 4.4.6
    """
    description = StringField("Plz introduce")
    detail = CKEditorField("Detail Description", validators=[DataRequired()])  # 富文本编辑器字段, Chapter 4.4.5
    images = MultipleFileField('UploadMoreImages',
                               validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submitimage = SubmitField("GoGo")
    tempsubmit = SubmitField("TempSave")  # 多个提交按钮演示, Chapter 4.4.6


class IntroducePictureForm(MyBaseForm):
    """
    Function: 单个页面多个表单的演示
    Chapter: 4.4.7
    """
    modelname = StringField("ModelName")
    modelpic = MultipleFileField("UploadPic", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submitmodel = SubmitField("Save")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

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
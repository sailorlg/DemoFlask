from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

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
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


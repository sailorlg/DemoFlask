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


class NewNoteListForm(MyBaseForm):
    """
    Function: 演示从页面读入提交的数据并保存到数据库的过程
              创建表单
    Chapter: 5.4.2_1~2
    """
    notebody = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditNoteForm(NewNoteListForm):
    """
    Function:演示修改一个已经显示在页面中的数据
    Chapter: 5.4.2_3
    """
    submit = SubmitField("Update")


class DeleteNoteForm(MyBaseForm):
    """
    Function:演示删除一个已经显示在页面中的数据
    Chapter: 5.4.2_4
    说明: 这里不能继承NewNoteListForm, 因为提交删除的时候, notebody会为空, 无法满足"validators=[DataRequired()]"的条件
    """
    submit = SubmitField("Delete")
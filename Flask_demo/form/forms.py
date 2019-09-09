from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 64)])
    remember = BooleanField('记住密码')
    submit = SubmitField('登录')

# 自定义验证器-行内验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('数字')
    submit = SubmitField()

    def valifate_answer(form, field):
        if field.data != 42:
            raise ValidationError('必须为42！')

# 自定义验证器-全局验证器
def is_42(form, field):
    if field.data != 42:
        raise ValidationError('必须为42！')

class FortyTwoForm2(FlaskForm):
    answer = IntegerField('数字')
    submit = SubmitField()


# 工厂函数形式的全局验证器示例
def is_42(message=None):
    if message is None:
        message = '必须为42！'

    def _is_42(form, field):
        if field.data != 42:
            raise ValidationError(message)

class FortyTwoForm3(FlaskForm):
    answer = IntegerField('数字', validators=[is_42()])
    submit = SubmitField()

# 上传文件
class UploadForm(FlaskForm):
    photo = FileField('上传图片', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField()

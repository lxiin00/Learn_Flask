from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditorField


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

# 上传多文件
class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('上传图片', validators=[DataRequired()])
    submit = SubmitField('提交')

# 富文本编辑器
class RichTextForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')

class NewPostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('内容', validators=[DataRequired()])
    save = SubmitField('保存')
    publish = SubmitField('发布')

class SigninForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 64)])
    submit1 = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 64)])
    submit2 = SubmitField('注册')

class SigninForm2(FlaskForm):
    username = StringField('用户明', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('登录')

class RegisterForm2(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('注册')


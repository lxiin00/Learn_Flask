from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


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

# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):  # 管理员登录
    name = StringField('账号', validators=[DataRequired(), Length(1, 20)])
    pswd = PasswordField('密码', validators=[DataRequired(), Length(6, 8)])
    remember = BooleanField('记住我')
    submit = SubmitField('提交')


class DevicesForm(FlaskForm):
    thsensor = BooleanField('温湿度传感器')
    ilsensor = BooleanField('光照度传感器')
    wdsensor = BooleanField('风速传感器')
    nosensor = BooleanField('噪声传感器')
    pmsensor = BooleanField('PM2.5传感器')
    light = BooleanField('路灯')
    submit = SubmitField('提交')



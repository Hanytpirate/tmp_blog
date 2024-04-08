from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名',[DataRequired(),Length(min=2,max=20)])
    email = StringField('电子邮件',[DataRequired(),Email()])
    password = PasswordField('密码',[DataRequired()])
    confirm_password = PasswordField('确认密码',[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("该用户名已被注册")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("该电子邮件已被使用")


class LoginForm(FlaskForm):
    email = StringField('电子邮件',[DataRequired(),Email()])
    password = PasswordField('密码',[DataRequired()])
    remember = BooleanField('记住密码')
    submit = SubmitField('登录')

class UpdateAccountForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('电子邮件',
                        validators=[DataRequired(), Email()])
    picture = FileField('更新头像', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('更新')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已被注册')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该电子邮件已被使用')
class PostForm(FlaskForm):
    title = StringField('题目', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')
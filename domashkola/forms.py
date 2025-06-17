from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    select_category = SelectField('Категория', coerce=int)
    category_id = IntegerField('Категория id')
    header = StringField('Заголовок карточки')
    body = TextAreaField('Текст карточки', validators=[DataRequired()])
    keywords = StringField('Ключевые слова')
    attached_files = StringField('Приложенные файлы')
    link = StringField('Ссылка на исходный пост')
    submit = SubmitField('Записать')


class PaginationPageForm(FlaskForm):
    input_page = IntegerField('input_page')
    submit = SubmitField('submit_btn')

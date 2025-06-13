from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from domashkola.auth import users, logger
from domashkola.forms import LoginForm
import sqlalchemy as sa
from domashkola import db
from domashkola.models import Users
from urllib.parse import urlsplit


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(Users).where(Users.username == form.username.data))
        if user is None or not user.check_password(password=form.password.data):
            logger.info("Пользователь {} или пароль {} введены неверно"
                        .format(form.username.data, form.password.data))
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template(url_for('users.login')+".html", title='Авторизация', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

from flask import render_template, flash, redirect, url_for

from domashkola.auth import users
from domashkola.auth.forms import LoginForm


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    page = "login"
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main.index'))
    print(form.username.data)
    return render_template(url_for('users.login')+".html", form=form, page=page)

from flask import render_template, url_for

from domashkola.main import main


@main.route('/')
@main.route('/index')
def index():
    return render_template(url_for('main.index')+".html")

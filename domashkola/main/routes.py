from flask import render_template, url_for
from flask_login import current_user, login_required
from domashkola.main import main
import sqlalchemy as sa
from domashkola import db
from domashkola.models import Categories, Posts

@main.route('/')
@main.route('/index')
@login_required
def index():
    page = 'главная страница'
    posts = db.session.scalars(sa.select(Posts).limit(3)).all()
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id)).all()
    return render_template(url_for('main.index')+".html", title="Домашняя школа - главная страница", page=page, posts=posts, categories=categories)

from flask import render_template, url_for
from flask_login import current_user, login_required
from domashkola.posts import posts
import sqlalchemy as sa
from domashkola import db
from domashkola.models import Categories, Posts


@posts.route('/posts_by_cat/<id>')
@login_required
def view_posts_by_category(id):
    page = db.session.get(Categories, int(id)).category_name
    posts = db.session.scalars(sa.select(Posts).filter(Posts.category_id == int(id)).order_by(Posts.timestamp.desc())).all()
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id)).all()
    return render_template(url_for('main.index')+".html", title=page, page=page, posts=posts, categories=categories)
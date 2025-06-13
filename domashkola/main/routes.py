from flask import render_template, url_for, request, current_app
from flask_login import login_required
from domashkola.main import main, logger
import sqlalchemy as sa
from domashkola import db
from domashkola.models import Categories, Posts
from domashkola.forms import PaginationPageForm


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    form = PaginationPageForm()
    if form.validate_on_submit():
        # logger.info("Введена страница: {}, {}".format(form.input_page.data, type(form.input_page.data)))
        page = form.input_page.data
    else:
        page = request.args.get('page', 1, type=int)
    
    # logger.info("page: {}, {}".format(page, type(page)))
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id.asc())).all()
    posts = db.paginate(sa.select(Posts).order_by(Posts.id.desc()), page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(url_for('main.index')+".html", title="Домашняя школа", 
                           posts=posts.items, next_url=next_url, prev_url=prev_url,
                           current_page=posts.page, qty_of_pages=posts.pages, 
                           form=form, categories=categories)

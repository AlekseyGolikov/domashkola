from flask import render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_required
from domashkola.posts import posts, logger
import sqlalchemy as sa
from domashkola import db
from domashkola.models import Categories, Posts
from domashkola.forms import PaginationPageForm


@posts.route('/view_posts/<category_id>', methods=['GET', 'POST'])
@login_required
def view_posts(category_id):

    form = PaginationPageForm()
    if form.validate_on_submit():
        # logger.info("Введена страница: {}, {}".format(form.input_page.data, type(form.input_page.data)))
        page = form.input_page.data
    else:
        page = request.args.get('page', 1, type=int)
    
    query = db.session.get(Categories, int(category_id)).posts.select().order_by(Posts.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id)).all()  
    title = db.session.get(Categories, int(category_id)).category_name.capitalize()

    next_url = url_for('posts.view_posts', category_id=category_id, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.view_posts', category_id=category_id, page=posts.prev_num) \
        if posts.has_prev else None


    return render_template('posts/view_posts.html', category_id=category_id, title=title, 
                            posts=posts.items, next_url=next_url, prev_url=prev_url, 
                            current_page=posts.page, qty_of_pages=posts.pages,
                            form=form, categories=categories, back_link=2)

@posts.route('/view_post/<post_id>/<back_link>/<category_id>')
@login_required
def view_post(post_id, back_link, category_id):
    post = db.session.get(Posts, int(post_id))
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id)).all()
    keywords_list = post.keywords[:-1].split(",")
    title = "Карточка поста"
    logger.info("post_id: {}, back_link: {}, category_id {}".format(post_id, back_link, category_id))
    return render_template('posts/view_post.html', title=title, post=post, keywords_list=keywords_list,
                            categories=categories, back_link=back_link, category_id=category_id)

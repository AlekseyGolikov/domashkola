from flask import render_template, url_for, request, current_app, flash, redirect
from flask_login import login_required
from domashkola.admin import admin, logger
from domashkola import db
from domashkola.models import Categories, Posts
from domashkola.forms import PostForm, PaginationPageForm
import sqlalchemy as sa
from sqlalchemy import union, case
from sqlalchemy.exc import SQLAlchemyError


@admin.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # logger.info("Путь к админке: {}".format(url_for("admin.index")))
    form = PaginationPageForm()

    if form.validate_on_submit():
        page = form.input_page.data
    else:
        page = request.args.get('page', 1, type=int)
    
    
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id.asc())).all()

    # сложный запрос: хочу вывести по сути 2 выборки, объединённые в одну
    # сначала хочу вывести список записей с категорией "Выберите категорию", отсортированных по времени, начиная с самых древних
    # затем должен идти список записей с заданными категориями, также отсортированных по времени, начиная с самых древних
    p1 = sa.select(Posts).filter(Posts.category_id == 1).order_by(Posts.timestamp.asc())
    p2 = sa.select(Posts).filter(Posts.category_id != 1).order_by(Posts.timestamp.asc())
    ids_list = db.session.scalars(p1.union(p2)).all()
    id_ordering = case(
        {_id: index for index, _id in enumerate(ids_list)},
        value=Posts.id
    )
    posts = db.paginate(sa.select(Posts).order_by(id_ordering), page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('admin.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('admin.index', page=posts.prev_num) \
        if posts.has_prev else None
    
    return render_template(url_for("admin.index")+'.html', title="Административная панель",
                            posts=posts.items, next_url=next_url, prev_url=prev_url, form=form,
                            current_page=posts.page, qty_of_pages=posts.pages, 
                            categories=categories, back_link=4)
                                            # back_link=1 - для возврата на main.index
                                            # back_link=2 - для возврата на posts.view_posts
                                            # back_link=3 - для возврата на posts.view_post
                                            # back_link=4 - для возврата на admin.index

@admin.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    form = PostForm()
    
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id.asc())).all()
    category_names = [(cat.id, cat.category_name) for cat in categories]
    # logger.info("category_names: {}".format(category_names))
    form.select_category.choices = category_names

    if form.validate_on_submit():
        try:
            logger.info("Ошибка {}".format(form.select_category.data))
            c = db.session.get(Categories, form.select_category.data)
            p = Posts(category=c, category_name=c.category_name, link=form.link.data, body=form.body.data, header=form.header.data, keywords=form.keywords.data)
            db.session.add(p)
            db.session.commit()
            flash("Карточка успешно записана в базу")
            return redirect(url_for('admin.index'))
        except SQLAlchemyError as e:
            flash("Ошибка записи в БД: " + str(e.__dict__['orig']))
        
        # logger.info("Для записи в БД: cat_name {}, header {}, body {}, kw {}".format(c.category_name, form.header.data, form.body.data[:20]+'...', form.keywords.data))
      
    return render_template(url_for("admin.insert")+'.html', title="Административная панель", 
                            form=form, categories=categories)


@admin.route('/update/<post_id>/<back_link>', methods=['GET', 'POST'])
@login_required
def update(post_id, back_link):
    form = PostForm()

    p = db.session.get(Posts, post_id)
    categories = db.session.scalars(sa.select(Categories).order_by(Categories.id.asc())).all()
    category_names = [(cat.id, cat.category_name) for cat in categories]
    form.select_category.choices = category_names

    if form.validate_on_submit():
        try:
            logger.info("form.select_category.data {}".format(form.select_category.data))
            p.category_id = category_names[form.select_category.data-1][0]
            p.category_name = category_names[form.select_category.data-1][1]
            p.header = form.header.data
            p.link = form.link.data
            p.keywords = form.keywords.data
            p.body = form.body.data
            p.attached_files = form.attached_files.data
            db.session.add(p)
            db.session.commit()
            logger.info("cat_id {}, cat_name {}, header {}, link {}, kw {}, body {}".format(p.category_id,
                                                                                            p.category_name,
                                                                                            p.header,
                                                                                            p.link,
                                                                                            p.keywords,
                                                                                            p.body[:20]+'...'))

            flash("Карточка успешно обновлена в базе")
            return redirect(url_for('admin.index'))
        except SQLAlchemyError as e:
            flash("Ошибка записи в БД: " + str(e.__dict__['orig']))
        
        # logger.info("Для записи в БД: cat_name {}, header {}, body {}, kw {}".format(c.category_name, form.header.data, form.body.data[:20]+'...', form.keywords.data))
      
    return render_template("admin/update.html", title="Административная панель", 
                           categories=categories, form=form, post=p, back_link=back_link)


@admin.route('/delete/<post_id>')
@login_required
def delete(post_id):
    try:
        p = db.session.get(Posts, post_id)
        db.session.delete(p)
        db.session.commit()
        flash("Запись успешно удалена")
        return redirect(url_for('admin.index'))
    
    except SQLAlchemyError as e:
        flash("Ошибка удаления записи из БД: " + str(e.__dict__['orig']))
        
        # logger.info("Для записи в БД: cat_name {}, header {}, body {}, kw {}".format(c.category_name, form.header.data, form.body.data[:20]+'...', form.keywords.data))
    
    return redirect(url_for('admin.index'))

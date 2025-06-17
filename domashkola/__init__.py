from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager
from queue import LifoQueue    # организация стека страничных переходов. Например, пагинированная выборка карточек -> Карточка записи. С помощью стэка возвращаемся в то самое место откуда вызывалась карточка


bootstrap = Bootstrap5()
db = SQLAlchemy()
login = LoginManager()
call_stack = LifoQueue()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    bootstrap.init_app(app)
    db.init_app(app)
    call_stack._init(app)
    login.init_app(app)
    login.login_view = 'users.login'
    migrate = Migrate(app, db)
    from domashkola import models

    from domashkola.main import main
    app.register_blueprint(main)
    from domashkola.admin import admin
    app.register_blueprint(admin, url_prefix='/admin')
    from domashkola.posts import posts
    app.register_blueprint(posts, url_prefix='/posts')
    from domashkola.auth import users
    app.register_blueprint(users, url_prefix='/auth')

    return app

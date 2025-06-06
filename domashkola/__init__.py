from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate


bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate(db)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    from domashkola import models

    from domashkola.main import main
    app.register_blueprint(main)
    from domashkola.auth import users
    app.register_blueprint(users, url_prefix='/auth')

    return app

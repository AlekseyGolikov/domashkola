import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, '.env'))

FLASK_ENV = os.environ['FLASK_ENV']
FLASK_APP = os.environ['FLASK_APP']
FLASK_DEBUG = os.environ['FLASK_DEBUG']
SECRET_KEY = os.environ['SECRET_KEY']

BOOTSTRAP_BOOTSWATCH_THEME = 'Lumen'   # Тема Bootstrap
POSTS_PER_PAGE = 3                      # Количество постов на странице

DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME

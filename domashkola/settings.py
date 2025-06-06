import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, '.env'))

FLASK_ENV = os.environ['FLASK_ENV']
FLASK_APP = os.environ['FLASK_APP']
DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ['SECRET_KEY']
BOOTSTRAP_BOOTSWATCH_THEME = 'United'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'domashkola.db')

from flask import Blueprint


main = Blueprint('main', __name__)

from domashkola.main import routes

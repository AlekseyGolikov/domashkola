from flask import Blueprint


users = Blueprint('users', __name__)

from domashkola.auth import routes

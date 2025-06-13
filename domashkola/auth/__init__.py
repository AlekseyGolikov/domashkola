from flask import Blueprint
import logging


users = Blueprint('users', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/{__name__}.log", mode='w', encoding='utf-8')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

from domashkola.auth import routes

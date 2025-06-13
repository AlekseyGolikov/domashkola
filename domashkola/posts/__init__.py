import logging
from flask import Blueprint


posts = Blueprint('posts', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/{__name__}.log", encoding='utf-8')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

from domashkola.posts import routes

from flask_babel import Babel
from flask import Flask
from .config import config

app = Flask(__name__)

app.config.update(config)

babel = Babel(app)

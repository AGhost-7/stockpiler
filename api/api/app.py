from flask_babel import Babel
from flask import Flask
from .config import config
from .validation import on_validation_error, ValidationError

app = Flask(__name__)

app.config.update(config)
app.errorhandler(ValidationError)(on_validation_error)

babel = Babel(app)

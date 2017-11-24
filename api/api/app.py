from flask_babel import Babel
from flask import Flask
from .config import config
from .validation import on_validation_error, ValidationError

app = Flask(__name__)


@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = config['BASE_URL']
    response.headers['Access-Control-Allow-Headers'] = \
        'Authorization,Content-Type'
    response.headers['Access-Control-Allow-Methods'] = \
        'GET,PUT,POST,DELETE,OPTIONS,PATCH'
    return response


app.config.update(config)
app.errorhandler(ValidationError)(on_validation_error)

babel = Babel(app)

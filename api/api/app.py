from .validation import on_validation_error, ValidationError
from flask_babel import Babel, gettext
from flask import Flask, jsonify
from .config import config
import traceback

app = Flask(__name__)


@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = config['BASE_URL']
    response.headers['Access-Control-Allow-Headers'] = \
        'Authorization,Content-Type'
    response.headers['Access-Control-Allow-Methods'] = \
        'GET,PUT,POST,DELETE,OPTIONS,PATCH'
    return response


@app.errorhandler(Exception)
def generic_error(error):
    traceback.print_exc()
    message = gettext('An unexpected internal error occured')
    response = jsonify(message=message)
    response.status_code = 500
    return response


app.errorhandler(ValidationError)(on_validation_error)

app.config.update(config)

babel = Babel(app)

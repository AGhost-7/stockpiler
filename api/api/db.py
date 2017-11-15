from .app import app
from flask_sqlalchemy import SQLAlchemy
from .base_model import BaseModel

db = SQLAlchemy(app, model_class=BaseModel)

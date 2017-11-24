
from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import declared_attr
import inflection


class BaseModel(Model):

    @declared_attr
    def __tablename__(cls):
        return inflection.underscore(cls.__name__)


# Utility for database transaction management since I need
# to use sqlalchemy more directly in my tests. Still pulls from
# the same configuration as the app, etc.

from sqlalchemy.orm import sessionmaker
from api.db import db
from contextlib import contextmanager


Session = sessionmaker(bind=db.engine, expire_on_commit=False)


@contextmanager
def create_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception():
        session.rollback()
        raise
    finally:
        session.close()

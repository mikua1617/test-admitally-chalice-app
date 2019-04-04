from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from chalicelib.db import db




@contextmanager
def get_session():
    session = sessionmaker(bind=db)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
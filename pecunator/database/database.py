from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config


engine = create_engine(config.DATABASE_URL())

Session = sessionmaker(engine)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()

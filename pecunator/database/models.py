from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    telegram_id = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id"))

    balance = Column(Integer)

    group = relationship("Group")
    operations = relationship("Operation")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)

    total_balance = Column(Integer)

    users = relationship("User")
    operations = relationship("Operation")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    datetime = Column(DateTime)

    author = relationship("User")
    group = relationship("Group")

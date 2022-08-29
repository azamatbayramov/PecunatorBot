from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    telegram_id = Column(String)
    group_id = Column(String, ForeignKey("groups.telegram_id"))
    username = Column(String)

    balance = Column(Integer)

    group = relationship("Group", back_populates="users")
    operations = relationship("Operation", back_populates="author")


class Group(Base):
    __tablename__ = "groups"

    telegram_id = Column(String, primary_key=True)

    total_balance = Column(Integer, default=0)

    users = relationship("User", back_populates="group")
    operations = relationship("Operation", back_populates="group")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(String, ForeignKey("groups.telegram_id"))

    amount = Column(Integer)
    label = Column(String)

    is_reset = Column(Boolean)

    datetime = Column(DateTime)

    author = relationship("User", back_populates="operations")
    group = relationship("Group", back_populates="operations")

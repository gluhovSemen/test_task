from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    eth_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    auth_token = relationship("AuthToken", uselist=False)
    __table_args__ = (
        CheckConstraint("password ~* '[0-9]' AND password ~* '[A-Z]'", name="password_format_check"),
        CheckConstraint("CHAR_LENGTH(password) >= 8", name="password_length_check"),
    )


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)

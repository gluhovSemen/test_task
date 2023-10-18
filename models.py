from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    eth_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    auth_token = relationship("AuthToken", uselist=False)
    __table_args__ = (
        CheckConstraint(
            "password ~* '[0-9]' AND password ~* '[A-Z]'", name="password_format_check"
        ),
        CheckConstraint("CHAR_LENGTH(password) >= 8", name="password_length_check"),
    )

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)

class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    user = relationship("Users", backref="contact")
    name = Column(String, index=True)
    surname = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    birthday = Column(Date, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

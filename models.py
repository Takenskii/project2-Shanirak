from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)
    name = Column(String)
    city = Column(String)

    # Связь с объявлениями
    shanyraks = relationship("Shanyrak", back_populates="owner")
    comments = relationship("Comment", back_populates="author")


class Shanyrak(Base):
    __tablename__ = "shanyraks"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    price = Column(Integer)
    address = Column(String)
    area = Column(Integer)
    rooms_count = Column(Integer)
    description = Column(Text)

    # Внешний ключ на пользователя, который создал объявление
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="shanyraks")

    # Связь с комментариями
    comments = relationship("Comment", back_populates="shanyrak")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(String)  # Для упрощения пока используем строку, позже можем добавить авто таймстемп
    shanyrak_id = Column(Integer, ForeignKey("shanyraks.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    shanyrak = relationship("Shanyrak", back_populates="comments")
    author = relationship("User", back_populates="comments")

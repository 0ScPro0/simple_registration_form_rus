from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime, BLOB, func
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

class Base(DeclarativeBase):
    created:Mapped[DATETIME] = mapped_column(DATETIME , default = func.now())
    updated: Mapped[DATETIME] = mapped_column(DATETIME , default = func.now() , onupdate = func.now())

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer(), primary_key = True)
    username: Mapped[str] = mapped_column(String(150), nullable = False)
    email: Mapped[str] = mapped_column(String(150), nullable = False)
    password: Mapped[str] = mapped_column(String(150), nullable = False)

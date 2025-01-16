from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

from sqlalchemy import Float


class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, primary_key=True)
    phone = Column(String)
    name = Column(String)
    password = Column(String)
    role = Column(String)
    userName = Column(String, unique=True, index=True)
    address = Column(String)
    image = Column(String)


class Resident(Base):
    __tablename__ = "residents"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    reward = Column(Integer, default=0)


class ReportWaste(Base):
    __tablename__ = "reportWaste"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, ForeignKey("users.email"))
    description = Column(String)
    location = Column(String)
    status = Column(String)
    date = Column(DateTime, default=datetime.utcnow)  # Changed to datetime.utcnow
    image = Column(ARRAY(String), nullable=False)
    reward = Column(Integer)


class ForgotPassword(Base):
    __tablename__ = "forgotPassword"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    token = Column(String, unique=True, index=True)
    expriesAt = Column(DateTime)




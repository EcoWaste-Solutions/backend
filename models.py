
from xmlrpc.client import Boolean
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, Text
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from sqlalchemy import DateTime

from sqlalchemy.dialects.postgresql import ARRAY



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
    date = Column(DateTime, default=datetime.now())
    image = Column(ARRAY(String), nullable=False)
    reward = Column(Integer)
    

    








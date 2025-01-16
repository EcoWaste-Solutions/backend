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



class RecycleInfo(Base):
    __tablename__ = "recycleInfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    waste_type = Column(String, nullable=False)  # "mixed waste (plastic, paper, organic, metal)"
    quantity = Column(String, nullable=False)    # "approximately 5000 kg"
    unit = Column(String, nullable=False)        # "kg" or "liters"
    confidence = Column(Float, nullable=False)   # 0.85
    description = Column(Text, nullable=True)    # "The image shows a large landfill..."
    location = Column(String, nullable=True)     # Optional for specific geographical details
    image = Column(ARRAY(String), nullable=True) # To store image URLs if necessary
    reported_at = Column(DateTime, default=datetime.utcnow)  # Ti
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
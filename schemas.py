from datetime import date

from typing import List
from pydantic import BaseModel, EmailStr
from typing import Union

from typing import Optional


class Token(BaseModel):
    accessToken: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr


class payload(BaseModel):
    email: EmailStr
    role: str
    phone: str
    name: str
    userName: str
    image: str

    class Config:
        orm_mode = True


class ResidentProfile(BaseModel):
    email: EmailStr
    phone: str
    name: str
    reward: int
    image: str
    address: str

    class Config:
        orm_mode = True


class ResidentSignup(BaseModel):
    email: EmailStr
    phone: str
    name: str
    password: str
    address: str
    image: str


class Signin(BaseModel):
    email: str
    password: str


class ReportWaste(BaseModel):
    description: str
    location: str
    image: List[str]

    class Config:
        orm_mode = True


class ReportWasteResponse(BaseModel):
    description: str
    location: str
    status: str
    date: date
    image: List[str]
    reward: int

    class Config:
        orm_mode = True

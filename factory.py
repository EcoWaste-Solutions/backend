from datetime import date

from typing import List
from pydantic import BaseModel, EmailStr
from typing import Union

from typing import Optional
import schemas
import utils
import models


class UserFactory:
    def createUser(resident: schemas.ResidentSignup):
        return models.User(
            email=resident.email,
            phone=resident.phone,
            name=resident.name,
            role="RESIDENT",
            image=resident.image,
            address=resident.address,
            userName=utils.createUserName(resident.name),
            password=utils.hash(resident.password),
        )

    def createAdmin():
        return models.User(
            email="dibbyoroy7@gmail.com",
            phone="01763157183",
            name="Dibbyo Roy",
            role="ADMIN",
            image="image",
            address="address",
            userName="dibbyoroy7",
            password=utils.hash("1234"),
        )


class ResidentFactory:
    def createResident(resident: schemas.ResidentSignup):
        return models.Resident(
            email=resident.email,
            phone=resident.phone,
            name=resident.name,
        )


class ReportWasteFactory:
    def createReportWaste(report: schemas.ReportWaste, email):
        return models.ReportWaste(
            email=email,
            description=report.description,
            location=report.location,
            status="PENDING",
            image=[url for url in report.image],
            reward=10
        )
    


class EdirtProfileFactory:
    def editProfile(user: schemas.UserEditProfile):
        return models.User(
            name=user.name,
            phone=user.phone,
            address=user.address,
            image=user.image
        )
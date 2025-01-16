import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from fastapi import File, UploadFile

from datetime import datetime

import base64
from fastapi import Form

from typing import List

import factory
import requests

import utils
import observer

router = APIRouter(tags=["Collector"], prefix="/collector")

from middileware import checkingRole

import processImg


@router.get("/getProfile", status_code=200, response_model=schemas.ResidentProfile)
def getProfile(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "COLLECTOR":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="USERNOTFOUND")

    collector = (
        db.query(models.Collector)
        .filter(models.Collector.email == currentUser.email)
        .first()
    )

    response = schemas.ResidentProfile(
        email=user.email,
        phone=user.phone,
        name=user.name,
        reward=collector.reward,
        image=user.image,
        address=user.address,
    )

    return response
# @router.put("/editProfile", status_code=201)
# def editProfile(
#     edit: schemas.UserEditProfile,
#     db: Session = Depends(database.get_db),
#     currentUser=Depends(oauth2.getCurrentUser),
# ):
#     if currentUser.role != "RESIDENT":
#         raise HTTPException(status_code=401, detail="UNAUTHORIZED")

#     user = db.query(models.User).filter(models.User.email == currentUser.email).first()

#     user.name = edit.name
#     user.phone = edit.phone
#     user.address = edit.address
#     user.image = edit.image

#     db.commit()
#     db.refresh(user)

#     auth_subject = observer.AuthSubject()

#     email_observer = observer.EmailNotificationObserver(user.email)
#     audit_log_observer = observer.AuditLogObserver()

#     auth_subject.add_observer(email_observer)
#     auth_subject.add_observer(audit_log_observer)

#     auth_subject.notify_observers(
#         subject="Profile Updated",
#         body=f"Profile updated successfully!",
#     )

#     return {"message": "SUCCESS"}

@router.put("/editProfile", status_code=201)

def editProfile(
    edit: schemas.UserEditProfile,
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser),
):
    if currentUser.role != "COLLECTOR":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="USERNOTFOUND")

    user.phone = edit.phone
    user.name = edit.name
    user.address = edit.address
    user.image = edit.image

    db.commit()
    db.refresh(user)

    auth_subject = observer.AuthSubject()


    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="PROFILEUPDATED",
        body=f"Hello {user.name}, Your profile has been updated successfully",
    )


    return {"message": "PROFILEUPDATED"}


@router.get("/getWasteReports", status_code=200)
def getWasteReports(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "COLLECTOR":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    reports = db.query(models.ReportWaste).filter(models.ReportWaste.status == "PENDING").all()

    return reports


import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


from datetime import datetime

from fastapi import Form

from typing import List
import middileware

from fastapi.responses import JSONResponse
from factory import EdirtProfileFactory

import observer
from pydantic import BaseModel, EmailStr

from middileware import checkingRole


router = APIRouter(tags=["Admin"], prefix="/admin")


@router.get("/getAllWasteReports")
def getAllWasteReports(
    db: Session = Depends(database.get_db), currentUser=Depends(checkingRole("ADMIN"))
):
    reports = db.query(models.ReportWaste).all()

    return reports


@router.get("/getProfile", status_code=200)
def getProfile(
    db: Session = Depends(database.get_db), currentUser=Depends(checkingRole("ADMIN"))
):
    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="USERNOTFOUND")

    response = schemas.UserProfile(
        email=user.email,
        phone=user.phone,
        name=user.name,
        image=user.image,
        address=user.address,
    )

    return response


@router.put("/editProfile", status_code=201)
def editProfile(
    edit: schemas.UserEditProfile,
    db: Session = Depends(database.get_db),
    currentUser=Depends(checkingRole("ADMIN")),
):
    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    user.name = edit.name
    user.phone = edit.phone
    user.address = edit.address
    user.image = edit.image

    db.commit()
    db.refresh(user)

    auth_subject = observer.AuthSubject()

    # Send welcome email

    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    # Register observers
    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    # Notify observers (e.g., send email, log the action)
    auth_subject.notify_observers(
        subject="Profile Updated",
        body=f"Profile updated successfully!",
    )

    return {"message": "SUCCESS"}


@router.post("/addCollector")
def addCollector(
    collector: schemas.Collector,
    db: Session = Depends(database.get_db),
    currentUser=Depends(checkingRole("ADMIN")),
):
    user = db.query(models.User).filter(models.User.email == collector.email).first()

    if user:
        raise HTTPException(status_code=404, detail="USERALREADYEXISTS")

    user = models.User(
        email=collector.email,
        phone=collector.phone,
        name=collector.name,
        password=utils.hash("1234"),
        role="COLLECTOR",
        userName=utils.createUserName(collector.name),
        address=collector.address,
        image=collector.image,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    res = models.Collector(
        email=collector.email,
        phone=collector.phone,
        name=collector.name,
        reward=0,
    )

    db.add(res)
    db.commit()
    db.refresh(res)

    auth_subject = observer.AuthSubject()

    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="Collector Added",
        body=f"Collector {user.name} has been added successfully!",
    )

    return {"message": "SUCCESS"}


class QrCode(BaseModel):
    qrcode: str
    id: int


@router.post("/addQrcode", status_code=201)
def addQrcode(
    qr: QrCode,
    db: Session = Depends(database.get_db),
    currentUser=Depends(checkingRole("ADMIN")),
):
    reportWaste = (
        db.query(models.ReportWaste)
        .filter(models.ReportWaste.id == qr.id)
        .update(
            {
                "qrCode": qr.qrcode,
                "qrCodeUpdatedAt": datetime.now(),
                "qrCodeAddedBy": currentUser.email,
            }
        )
    )

    reportWaste = (
        db.query(models.ReportWaste).filter(models.ReportWaste.id == qr.id).first()
    )

    db.commit()

    auth_subject = observer.AuthSubject()

    email_observer = observer.EmailNotificationObserver(reportWaste.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="QR Code Added",
        body=f"QR Code has been added successfully!",
    )

    return {"message": "SUCCESS"}





class getReport(BaseModel):
    area : str
@router.get("/getReportsByArea", status_code=200)
def getReportsByArea(
    getReport: getReport,
    db: Session = Depends(database.get_db),
    currentUser=Depends(checkingRole("ADMIN")),
):
    reports = (
        db.query(models.ReportWaste)
        .filter(models.ReportWaste.location == getReport.area)
        .all()
    )

    return reports

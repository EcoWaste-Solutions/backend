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

router = APIRouter(tags=["Resident"], prefix="/resident")

from middileware import checkingRole

import processImg


@router.get("/getProfile", status_code=200, response_model=schemas.ResidentProfile)
def getProfile(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="USERNOTFOUND")

    resident = (
        db.query(models.Resident)
        .filter(models.Resident.email == currentUser.email)
        .first()
    )

    response = schemas.ResidentProfile(
        email=user.email,
        phone=user.phone,
        name=user.name,
        reward=resident.reward,
        image=user.image,
        address=user.address,
    )

    return response


@router.post("/getDescription", status_code=201)
def getDescription(
    img: schemas.Only_image,
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser),
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    response = requests.get(img.image)
    response.raise_for_status()
    image_data = base64.b64encode(response.content).decode("utf-8")
    waste_details = processImg.process_image(image_data)
    description = waste_details  # Use AI-generated waste details as description

    return description

    # Retrieve the user from the database


@router.post(
    "/reportWaste/",
    status_code=201,
    response_model=schemas.ReportWasteResponse,
)
def reportWaste(  # path parameter to control description logic
    report: schemas.ReportWaste,  # report data, including the image URL
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser),
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    # Retrieve the user from the database
    user = (
        db.query(models.Resident)
        .filter(models.Resident.email == currentUser.email)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    # Award the user 10 points for reporting
    user.reward += 10
    db.commit()
    db.refresh(user)

    # Determine the description source based on the `desc` parameter

    # Create the report entry
    reportWaste = factory.ReportWasteFactory.createReportWaste(
        report, currentUser.email
    )

    # Prepare the response data
    reportWasteResponse = schemas.ReportWasteResponse(
        description=reportWaste.description,
        location=reportWaste.location,
        status=reportWaste.status,
        date=datetime.now().date(),
        image=reportWaste.image,
        reward=reportWaste.reward,
    )

    # Save the report to the database
    db.add(reportWaste)
    db.commit()
    db.refresh(reportWaste)

    
    
   
    # Notify observers
    auth_subject = observer.AuthSubject()
    email_observer = observer.EmailNotificationObserver(currentUser.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="Report Waste",
        body=f"Hello {currentUser.name}, Your waste has been reported successfully",
    )

    return reportWasteResponse


@router.get("/getReports", status_code=200)
def getReports(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    reports = (
        db.query(models.ReportWaste)
        .filter(models.ReportWaste.email == currentUser.email)
        .all()
    )

    return [reports]


@router.put("/editProfile", status_code=201)
def editProfile(
    edit: schemas.UserEditProfile,
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser),
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    user = db.query(models.User).filter(models.User.email == currentUser.email).first()

    user.name = edit.name
    user.phone = edit.phone
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
        subject="Profile Updated",
        body=f"Profile updated successfully!",
    )

    return {"message": "SUCCESS"}

import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from image import image_to_base64

from fastapi import File, UploadFile
import shutil

from datetime import datetime

import base64
from fastapi import Form

from typing import List


router = APIRouter(
    tags=["Resident"],
    prefix="/resident"
)


@router.get("/getProfile", status_code=200, response_model=schemas.ResidentProfile)
def getProfile(
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(
            status_code=401, detail="UNAUTHORIZED"
        )

    user = db.query(models.User).filter(
        models.User.email == currentUser.email).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="USERNOTFOUND"
        )
    
    resident = db.query(models.Resident).filter(
        models.Resident.email == currentUser.email).first()
    
    response = schemas.ResidentProfile(
        email=user.email,
        phone=user.phone,
        name=user.name,
        reward=resident.reward,
        image=user.image,
        address=user.address
    )

    return response


@router.post("/reportWaste", status_code=201, response_model=schemas.ReportWasteResponse)
def reportWaste(
    report: schemas.ReportWaste,
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(
            status_code=401, detail="UNAUTHORIZED"
        )

    if db.query(models.User).filter(models.User.email != currentUser.email).first():
        raise HTTPException(
            status_code=400, detail="EMAILERROR"
        )

    user = db.query(models.Resident).filter(
        models.Resident.email == currentUser.email).first()

    if user:
        user.reward += 10
        db.commit()
        db.refresh(user)

    reportWaste = models.ReportWaste(
        email=currentUser.email,
        description=report.description,
        location=report.location,
        status="PENDING",
        image=[url for url in report.image],
        reward=10
    )

    reportWasteResponse = schemas.ReportWasteResponse(
        description=reportWaste.description,
        location=reportWaste.location,
        status=reportWaste.status,
        date=datetime.now().date(),  # Ensure only the date part is used
        image=reportWaste.image,
        reward=reportWaste.reward
    )

    db.add(reportWaste)
    db.commit()
    db.refresh(reportWaste)

    utils.sendEmail(
        "Waste Reported",
        f"Your waste report has been received. You will be rewarded with 10 points.",
        currentUser.email
    )

    return reportWasteResponse


@router.get("/getReports", status_code=200)
def getReports(
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser)
):
    if currentUser.role != "RESIDENT":
        raise HTTPException(
            status_code=401, detail="UNAUTHORIZED"
        )

    reports = db.query(models.ReportWaste).filter(
        models.ReportWaste.email == currentUser.email).all()

    return [reports]

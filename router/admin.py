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


router = APIRouter(tags=["Admin"], prefix="/admin")


@router.get("/getAllWasteReports")
def getAllWasteReports(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if middileware.checkingRole(currentUser, "ADMIN"):
        return db.query(models.ReportWaste).all()

@router.get("/getProfile", status_code=200)
def getProfile(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if middileware.checkingRole(currentUser, "ADMIN"):
        user = db.query(models.User).filter(models.User.email == currentUser.email).first()

        if not user:
            raise HTTPException(status_code=404, detail="USERNOTFOUND")

       
    return JSONResponse(content={"email": user.email, "phone": user.phone, "name": user.name, "image": user.image, "address": user.address})


@router.put("/editProfile", status_code=201)
def editProfile(
    edit:schemas.UserEditProfile,
    db: Session = Depends(database.get_db),
    currentUser=Depends(oauth2.getCurrentUser),
):
    if middileware.checkingRole(currentUser, "ADMIN"):
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


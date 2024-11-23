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

import factory

import observer


import uuid
from datetime import datetime, timedelta

import base64

from fastapi import Form


router = APIRouter(tags=["Authentication"])




@router.post("/signup", status_code=201)
def signup(resident: schemas.ResidentSignup, db: Session = Depends(database.get_db)):
    # Check if user already exists
    if db.query(models.User).filter(models.User.email == resident.email).first():
        raise HTTPException(status_code=400, detail="EMAILERROR")

    # Convert image to Base64

    # Prepare phone number

    # Create user in the database
    user = factory.UserFactory.createUser(resident)

    db.add(user)
    db.commit()
    db.refresh(user)

    res = factory.ResidentFactory.createResident(resident)
    db.add(res)
    db.commit()
    db.refresh(res)

    auth_subject = observer.AuthSubject()


    # Send welcome email

    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    # Register observers
    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    # Notify observers (e.g., send email, log the action)
    auth_subject.notify_observers(
        subject="Welcome to the System",
        body=f"Welcome {user.name}, your account has been successfully created!",
    )
    return {"message": "SUCCESS"}


@router.post("/signin")
def signin(credential: schemas.Signin, db: Session = Depends(database.get_db)):
    user = (
        db.query(models.User)
        .filter(
            (models.User.email == credential.email)
            | (models.User.userName == credential.email)
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="NOTFOUND")

    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=404, detail="PASSWORDERROR")
    print(user.role)

    access_token = oauth2.createAccessToken(
        data={
            "email": user.email,
            "role": user.role,
            "name": user.name,
            "phone": user.phone,
            "userName": user.userName,
            "image": user.image,
        }
    )

    tokenData = schemas.Token(accessToken=access_token, token_type="Bearer")
    return tokenData


@router.post("/forgotPassword")
def forgotPassword(
    cred: schemas.ForgotPassword, db: Session = Depends(database.get_db)
):
    email = cred.email
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="NOTFOUND")

    otp = str(uuid.uuid4().int)[:6]
    expriesAt = datetime.now() + timedelta(minutes=30)

    passwordReset = models.ForgotPassword(email=email, token=otp, expriesAt=expriesAt)

    db.add(passwordReset)

    db.commit()
    
    auth_subject = observer.AuthSubject()

    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="Password Reset",
        body=f"Hello {user.name}, Your password reset token is {otp}",
    )


    return {"message": "SUCCESS"}


@router.post("/resetPassword/{otp}")
def resetPassword(
    otp: str, cred: schemas.ResetPassword, db: Session = Depends(database.get_db)
):
    password = cred.password
    passwordReset = (
        db.query(models.ForgotPassword)
        .filter(models.ForgotPassword.token == otp)
        .first()
    )

    if not passwordReset:
        raise HTTPException(status_code=404, detail="NOTFOUND")

    if datetime.now() > passwordReset.expriesAt:
        raise HTTPException(status_code=400, detail="EXPIRED")

    user = (
        db.query(models.User).filter(models.User.email == passwordReset.email).first()
    )

    user.password = utils.hash(password)

    # Delete the password reset token
    db.delete(passwordReset)
    db.commit()

    auth_subject = observer.AuthSubject()

    email_observer = observer.EmailNotificationObserver(user.email)
    audit_log_observer = observer.AuditLogObserver()

    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    auth_subject.notify_observers(
        subject="Password Reset",
        body=f"Hello {user.name}, Your password has been successfully reset",
    )
    

    return {"message": "SUCCESS"}

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


import uuid
from datetime import datetime, timedelta

import base64

from fastapi import Form



router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup", status_code=201)
def signup(
    resident: schemas.ResidentSignup,
    db: Session = Depends(database.get_db)
):
    # Check if user already exists
    if db.query(models.User).filter(models.User.email == resident.email).first():
        raise HTTPException(
            status_code=400, detail="EMAILERROR")

    userName = utils.createUserName(resident.name)

    # Convert image to Base64

    # Prepare phone number
    phone = "+88" + resident.phone

    # Create user in the database
    user = models.User(
        email=resident.email,
        phone=phone,
        name=resident.name,
        password=utils.hash(resident.password),
        role="RESIDENT",
        userName=userName,
        address=resident.address,
        image=resident.image, 

    )

    db.add(user)
    db.commit()
    db.refresh(user)

    res = models.Resident(
        email=resident.email,
        phone=phone,
        name=resident.name,
    )
    db.add(res)
    db.commit()
    db.refresh(res)

    # Send welcome email
    utils.sendEmail(
        "Welcome to our platform",
        f"Hello {resident.name}, Welcome to our platform. Your username is {userName}.",
        resident.email
    )

    return {"message": "SUCCESS"}




@router.post("/signin")
def signin(
    credential: schemas.Signin,
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter((models.User.email == credential.email) | (
        models.User.userName == credential.email)).first()

    if not user:
        raise HTTPException(status_code=404, detail="NOTFOUND")
    
    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=404, detail="PASSWORDERROR")


    access_token = oauth2.createAccessToken(
        data={"email": user.email, "role": user.role, "name": user.name, "phone": user.phone, "userName": user.userName, "image": user.image})

    tokenData = schemas.Token(accessToken=access_token, token_type="Bearer")
    return tokenData

@router.post("/forgotPassword")
def forgotPassword(
    cred: schemas.ForgotPassword,
    db: Session = Depends(database.get_db)
):
    email = cred.email
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="NOTFOUND")
    
    otp = str(uuid.uuid4().int)[:6]
    expriesAt = datetime.now() + timedelta(minutes=30)


    passwordReset = models.ForgotPassword(
        email=email,
        token=otp,
        expriesAt=expriesAt
    )


    db.add(passwordReset)

    db.commit()
    utils.sendEmail(
        "Password Reset",
        f"Hello {user.name}, Your password reset otp is {otp}.",
        user.email
    )


    return {"message": "SUCCESS"}



@router.post("/resetPassword/{otp}")
def resetPassword(
    otp: str,
    cred: schemas.ResetPassword,
    db: Session = Depends(database.get_db)
):
    password = cred.password
    passwordReset = db.query(models.ForgotPassword).filter(models.ForgotPassword.token == otp).first()

    if not passwordReset:
        raise HTTPException(status_code=404, detail="NOTFOUND")
    
    if datetime.now() > passwordReset.expriesAt:
        raise HTTPException(status_code=400, detail="EXPIRED")

    user = db.query(models.User).filter(models.User.email == passwordReset.email).first()

    user.password = utils.hash(password)

    # Delete the password reset token
    db.delete(passwordReset)
    db.commit()

    utils.sendEmail(
        "Password Reset",
        f"Hello {user.name}, Your password has been reset successfully.",
        user.email
    )

    return {"message": "SUCCESS"}

from models import Start
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import factory
import requests
import utils
import observer

from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/start",
    tags=["db setup"],
    responses={404: {"description": "Route not found"}},
)


@router.post("/")
async def setup_db(
    db: Session = Depends(database.get_db),
):
    start_entry = db.query(Start).first()
    if start_entry: 
        return JSONResponse(
            status_code=400, content={"message": "Database already setup."}
        )
    
    start = Start(flag=True)

    db.add(start)

    db.commit()
    
    # Create admin user
    admin = factory.UserFactory.createAdmin()
    db.add(admin)
    db.commit()
    db.refresh(admin)



    email_observer = observer.EmailNotificationObserver("dibbyoroy7@gmail.com")
    audit_log_observer = observer.AuditLogObserver()

    auth_subject = observer.AuthSubject()

    # Register observers
    auth_subject.add_observer(email_observer)
    auth_subject.add_observer(audit_log_observer)

    # Notify observers (e.g., send email, log the action)
    auth_subject.notify_observers(
        subject="Welcome to the System",
        body=f"Welcome {"Dibbyo"}, your account has been successfully created!",
    )

    return JSONResponse(
        status_code=201, content={"message": "Database setup successful."}
    )




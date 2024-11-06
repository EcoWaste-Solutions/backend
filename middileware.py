import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


def checkingRole(currentUser, role):
    if currentUser.role != role:
        raise HTTPException(
            status_code=401, detail="UNAUTHORIZED"
        )
    return True

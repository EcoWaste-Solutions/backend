# middleware.py
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import oauth2
import database

def checkingRole(required_role: str):
    """
    Middleware to check the role of the current user.
    """
    def check_role(currentUser=Depends(oauth2.getCurrentUser), db: Session = Depends(database.get_db)):
        if currentUser.role != required_role:
            raise HTTPException(status_code=401, detail="UNAUTHORIZED")
        return currentUser

    return check_role
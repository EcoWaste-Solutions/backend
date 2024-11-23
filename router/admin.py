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

from fastapi import Form

from typing import List
import middileware


router = APIRouter(tags=["Admin"], prefix="/admin")


@router.get("/getAllWasteReports")
def getAllWasteReports(
    db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)
):
    if middileware.checkingRole(currentUser, "ADMIN"):
        return db.query(models.ReportWaste).all()

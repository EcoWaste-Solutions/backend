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
from middileware import checkingRole


router = APIRouter(tags=["all"], prefix="/leaderBoard")


@router.get("/leaderBoard", status_code=200)
def leaderBoard(db: Session = Depends(database.get_db)):
    residents = db.query(models.Resident).order_by(models.Resident.reward.desc()).all()
    response = []
    for resident in residents:
        response.append(
            schemas.LeaderBoard(
                name=resident.name,
                reward=resident.reward,
            )
        )

    return response

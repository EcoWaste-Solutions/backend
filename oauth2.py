from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import schemas
import database
import models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import config


settings = config.Settings()

oauthScheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 24*60


def createAccessToken(data: dict):

    toEncode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT


def verifyAccessToken(Token: str, credentialException):

    try:
        payload = jwt.decode(Token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("email")
        if email is None:
            raise credentialException
        tokenData = schemas.TokenData(email=email)
    except JWTError as e:
        print(e)
        raise credentialException

    return tokenData


def getCurrentUser(token: str = Depends(oauthScheme), db: Session = Depends(database.get_db)):
    credentialException = HTTPException(status_code=404,
                                        detail="Token is invalid",
                                        headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentialException)
    user = db.query(models.User).filter(
        models.User.email == token.email).first()
    return user

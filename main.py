
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


import models
import utils
from database import engine

from router import auth, resident

import config


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

manager = utils.connectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

app.include_router(auth.router)

app.include_router(resident.router)




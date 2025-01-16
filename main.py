
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
import utils
from database import engine

from router import auth, resident, admin, leaderBoard, collector

# import config




app = FastAPI()

manager = utils.connectionManager()


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://inventory.alvereduan.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
    

app.include_router(auth.router)

app.include_router(resident.router)

app.include_router(admin.router)

app.include_router(leaderBoard.router)

app.include_router(collector.router)






import httpx
import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import FastAPI
import random
from fastapi import Depends
from datetime import date, timedelta, datetime
from enum import Enum
import models
import database
from passlib.context import CryptContext
from datetime import datetime, timedelta
from email.message import EmailMessage
import ssl
import smtplib
from config import settings 


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


logging.basicConfig(level=logging.INFO)


# settings = config.Settings()  # Create an instance of the Settings class
emailSender = settings.email_sender
emailPassword = settings.email_password

def hash(password: str):
    return pwdContext.hash(password)


def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)


class connectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.active_connections.append(
            {"websocket": websocket, "email": email})

    def disconnect(self, websocket: WebSocket):
        self.connections = [
            connection for connection in self.active_connections if connection["websocket"] != websocket]

    async def sendPersonalMessage(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender_email: str, receiver_email: str):
        for connection in self.active_connections:
            if connection["email"] == receiver_email:
                await self.sendPersonalMessage(f"{sender_email}: {message}", connection["websocket"])


def createUserName(name: str):
    name = name.lower()
    name = name.split(" ")
    if len(name) == 1:
        userName = name[0]+str(random.randint(0, 9999))

    else:
        userName = name[0]+name[1]+str(random.randint(0, 9999))
    return userName

# send message to user


def sendEmail(subject: str, body: str, receiver_email: str):
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = emailSender
    message["To"] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(emailSender, emailPassword)
        server.send_message(message)



    
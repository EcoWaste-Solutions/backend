
from typing import List
import utils

class Observer:
    def update(self, subject: str, body: str):
        raise NotImplementedError("Subclasses should implement this method")

# Email Notification Observer
class EmailNotificationObserver(Observer):
    def __init__(self, user_email: str):
        self.user_email = user_email

    def update(self, subject: str, body: str):
        # Send an email using your existing `utils.sendEmail` method
        utils.sendEmail(subject, body, self.user_email)

# Audit Log Observer
class AuditLogObserver(Observer):
    def update(self, subject: str, body: str):
        # Log the action with a unified signature
        print(f"Audit Log - Subject: {subject}, Body: {body}")




class AuthSubject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, subject: str, body: str):
        for observer in self._observers:
            observer.update(subject, body)
from App.ext import db
from App.models import BaseModel


class Message(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    sendId = db.Column(db.String(16))
    receiveId = db.Column(db.String(16))
    content = db.Column(db.String(1024))
    status = db.Column(db.String(4), default='0')
    date = db.Column(db.DateTime)

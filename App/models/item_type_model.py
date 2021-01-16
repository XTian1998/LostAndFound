from App.ext import db
from App.models import BaseModel


class ItemType(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(32), unique=True)

from App.models import BaseModel
from App.ext import db


class Admin(BaseModel):
    id = db.Column(db.String(16), primary_key=True, unique=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))
    is_delete = db.Column(db.Boolean, default=False)
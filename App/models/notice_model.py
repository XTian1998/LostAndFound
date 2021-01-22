from App.ext import db
from App.models import BaseModel


class Notice(BaseModel):
    id = db.Column(db.String(32), primary_key=True)
    title =db.Column(db.String(128))
    content = db.Column(db.String(1024))
    type = db.Column(db.String(32))
    creator = db.Column(db.String(32))
    date = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

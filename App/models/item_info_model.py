from App.ext import db
from App.models import BaseModel
from App.models.item_type_model import ItemType
from App.models.user_model import User


class ItemInfo(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    info = db.Column(db.String(16))
    type = db.Column(db.String(16), db.ForeignKey(ItemType.type))
    image = db.Column(db.String(128))
    desc = db.Column(db.String(1024))
    date = db.Column(db.DateTime)
    place = db.Column(db.String(64))
    campus = db.Column(db.String(32))
    uid = db.Column(db.String(16), db.ForeignKey(User.id))
    is_claim = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)
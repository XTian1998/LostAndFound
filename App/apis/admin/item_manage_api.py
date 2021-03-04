import datetime

from flask import g
from flask_restful import Resource, reqparse

from App.models.item_info_model import ItemInfo
from App.models.message_model import Message
from App.utils import error_info, admin_login_required

parse_del = reqparse.RequestParser()
parse_del.add_argument('id', type=str, help='请提供信息编号')


class ItemManageResource(Resource):
    @admin_login_required
    def delete(self):
        args = parse_del.parse_args()
        id = args.get('id')
        item_info = ItemInfo.query.filter(ItemInfo.id == id, ItemInfo.is_delete == False).first()
        if not item_info:
            return error_info(400, '操作失败')
        item_info.is_delete = True
        item_info.save()

        msg = Message()
        msg.content = "您好，你的编号为"+ id+ "的启事已被管理员强制删除，如有疑问请及时联系管理员。"
        msg.sendId = g.user.id
        msg.date = datetime.datetime.now()
        msg.receiveId = item_info.uid
        msg.id = msg.receiveId + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if not msg.save():
            return error_info(400, '操作失败')

        return {
            "data": {
                "id": item_info.id,
                "uid": item_info.uid
            },
            "meta": {
                "status": 204,
                "msg": "删除成功"
            }
        }

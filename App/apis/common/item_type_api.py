from flask_restful import Resource, reqparse

from App.models.item_type_model import ItemType
from App.utils import error_info, admin_login_required

parse = reqparse.RequestParser()
parse.add_argument("type", type=str, required=True, help="请提供分类名称")


class ItemTypeResource(Resource):
    @admin_login_required
    def post(self):
        args = parse.parse_args()
        type = args.get('type')

        if ItemType.query.filter(ItemType.type == type).first():
            return error_info(400, "该分类已存在")
        item_type = ItemType()
        item_type.type = type
        if not item_type.save():
            return error_info(400, "添加分类失败")

        data = {
            "data": {
                "id": item_type.id,
                "category": item_type.type
            },
            "meta": {
                "status": 201,
                "msg": "添加分类成功"
            }
        }
        return data

    @admin_login_required
    def delete(self):
        args = parse.parse_args()
        type = args.get('type')

        item_type = ItemType.query.filter(ItemType.type == type).first()
        if not item_type:
            return error_info(400, "该分类不存在")
        if not item_type.delete():
            return error_info(400, "无法删除")

        data = {
            "data": None,
            "meta": {
                "status": 204,
                "msg": "删除分类成功"
            }
        }
        return data
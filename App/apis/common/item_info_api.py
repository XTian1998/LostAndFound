import datetime

from flask import g
from flask_restful import Resource, reqparse, fields, marshal, inputs

from App.models.item_info_model import ItemInfo
from App.models.item_type_model import ItemType
from App.models.message_model import Message
from App.models.user_model import User
from App.settings import session
from App.utils import error_info, user_login_required

parse = reqparse.RequestParser()
parse.add_argument('operation', type=str, required=True, help='请提供操作类型')
parse.add_argument('oid', type=str, help='请提供原信息编号')
parse.add_argument('info', type=str, required=True, help='请提供信息类型')
parse.add_argument('type', type=str, required=True, help='请提供物品类型')
parse.add_argument('desc', type=str, required=True, help='请提供物品描述')
parse.add_argument('campus', type=str, required=True, help='请提供校区参数')
parse.add_argument('image', type=str, help='请提供图片路径')
parse.add_argument('date', required=True, help='请提供时间')
parse.add_argument('place', type=str, required=True, help='请提供地点')
parse.add_argument('name', type=str, help='请提供姓名')

parse_del = reqparse.RequestParser()
parse_del.add_argument('id', type=str, help='请提供信息编号')

parse_claim = reqparse.RequestParser()
parse_claim.add_argument('id', type=str, help='请提供信息编号')

parse_query = reqparse.RequestParser()
parse_query.add_argument("pagenum", type=int, required=True, help="请提供pagenum参数")
parse_query.add_argument("pagesize", type=int, required=True, help="请提供pagesize参数")
parse_query.add_argument('id', type=str, help='请提供信息编号')
parse_query.add_argument('info', type=str, help='请提供信息类型')
parse_query.add_argument('type', type=str, help='请提供物品类型')
parse_query.add_argument('desc', type=str, help='请提供物品描述')
parse_query.add_argument('campus', type=str, help='请提供校区参数')
parse_query.add_argument('uid', type=str, help='请提供用户id')
parse_query.add_argument('date', type=int, help='请提供时间')
parse_query.add_argument('place', type=str, help='请提供地点')
parse_query.add_argument('is_claim',  type=inputs.boolean, help='请提供认领状态')
parse_query.add_argument('is_delete',  type=inputs.boolean, help='请提供删除状态')
parse_query.add_argument('image',  type=inputs.boolean, help='请提供删除状态')

item_info_fields = {
    "id": fields.String,
    "info": fields.String,
    "type": fields.String,
    "desc": fields.String,
    "campus": fields.String,
    "uid": fields.String,
    "username": fields.String,
    "phone": fields.String,
    "image": fields.String,
    "date": fields.DateTime,
    "place": fields.String,
    "is_claim": fields.Boolean,
    "is_delete": fields.Boolean,
}

item_info_list_fields = {
    "total": fields.Integer,
    "pagenum": fields.Integer,
    "pagesize": fields.Integer,
    "item_info_list": fields.List(fields.Nested(item_info_fields)),
}


class ItemInfoResource(Resource):
    @user_login_required
    def post(self):
        args = parse.parse_args()

        if args.get('operation') == 'repost' and args.get('oid') and ItemInfo.query.filter(ItemInfo.id == args.get('oid'), ItemInfo.is_delete == False, ItemInfo.uid == g.user.id).first():
            old_item = ItemInfo.query.filter(ItemInfo.id == args.get('oid'), ItemInfo.is_delete == False, ItemInfo.uid == g.user.id).first()
            old_item.is_delete = True
            item_info = ItemInfo()
            item_info.info = args.get('info')
            item_info.type = args.get('type')
            item_info.desc = args.get('desc')
            item_info.campus = args.get('campus')
            item_info.uid = g.user.id
            item_info.image = args.get('image')
            item_info.date = args.get('date')
            item_info.place = args.get('place')
            item_info.id = item_info.uid + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not item_info.save() and old_item.save():
                return error_info(400, '请检查参数')

        elif args.get('operation') == 'post':
            item_info = ItemInfo()
            item_info.info = args.get('info')
            item_info.type = args.get('type')
            item_info.desc = args.get('desc')
            item_info.campus = args.get('campus')
            item_info.uid = g.user.id
            item_info.image = args.get('image')
            item_info.date = datetime.datetime.strptime(args.get('date'), '%Y-%m-%d')
            item_info.place = args.get('place')
            item_info.id = item_info.uid + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not item_info.save():
                return error_info(400, '请检查参数')
            if args.get('name') and User.query.filter(User.name == args.get('name'), User.is_delete == False).first():
                receive_user = User.query.filter(User.name == args.get('name')).first()
                message = Message()
                message.sendId = '00000'
                message.receiveId = receive_user.id
                message.content = '系统检测到有人捡到了您的有关证件，信息编号为' + item_info.id + '，请及时与拾主进行联系。'
                message.date = datetime.datetime.now()
                message.id = message.receiveId + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                message.save()

        else:
            return error_info(400, '参数错误')
        data = {
            "data": marshal(item_info, item_info_fields),
            "meta": {
                "status": 201,
                "msg": "发布成功"
            }
        }
        return data

    @user_login_required
    def put(self):
        args = parse_claim.parse_args()

        item = ItemInfo.query.filter(ItemInfo.id == args.get('id'), ItemInfo.is_delete == False, ItemInfo.is_claim == False, ItemInfo.uid == g.user.id).first()
        if item:
            item.is_claim = True
            item.claim_date = datetime.datetime.now().date()
            item.save()
            return {
                "data": marshal(item, item_info_fields),
                "meta": {
                    "status": 201,
                    "msg": "认领成功"
                }
            }
        return error_info(400, "操作失败")

    @user_login_required
    def delete(self):
        args = parse_del.parse_args()
        id = args.get('id')
        item_info = ItemInfo.query.filter(ItemInfo.id == id, ItemInfo.uid == g.user.id, ItemInfo.is_delete == False).first()

        if not item_info:
            return error_info(400, '操作失败')

        item_info.is_delete = True
        item_info.save()

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

    def get(self):
        args= parse_query.parse_args()
        pagenum = args.get("pagenum")
        pagesize = args.get("pagesize")
        item_info = session.query(ItemInfo, User.phone, User.username).join(User).filter(User.id == ItemInfo.uid)
        if args.get('id'):
            item_info = item_info.filter(ItemInfo.id == args.get('id'))
        if args.get('info'):
            item_info = item_info.filter(ItemInfo.info == args.get('info'))
        if args.get('type'):
            item_info = item_info.filter(ItemInfo.type == args.get('type'))
        if args.get('campus'):
            item_info = item_info.filter(ItemInfo.campus == args.get('campus'))
        if args.get('uid'):
            item_info = item_info.filter(ItemInfo.uid == args.get('uid'))
        if args.get('is_claim') or str(args.get('is_claim')) == 'False':
            item_info = item_info.filter(ItemInfo.is_claim == args.get('is_claim'))
        if args.get('is_delete') or str(args.get('is_delete')) == 'False':
            item_info = item_info.filter(ItemInfo.is_delete == args.get('is_delete'))
        if args.get('date'):
            item_info = item_info.filter(ItemInfo.date >= datetime.datetime.now() - datetime.timedelta(days=args.get('date')))
        if args.get('place'):
            item_info = item_info.filter(ItemInfo.place == args.get('place'))
        if args.get('desc'):
            if (item_info.filter(ItemInfo.id == args.get('desc')).first()):
                item_info =item_info.filter(ItemInfo.id == args.get('desc'))
            elif (item_info.filter(ItemInfo.uid == args.get('desc')).first()):
                item_info =item_info.filter(ItemInfo.uid == args.get('desc'))
            else:
                item_info = item_info.filter(ItemInfo.desc.like("%"+args.get('desc')+"%"))
        if args.get('image'):
            item_info = item_info.filter(ItemInfo.image != '')

        total = item_info.count()
        item_info_list = item_info.order_by(ItemInfo.date.desc()).offset(pagesize* (pagenum-1)).limit(pagesize)
        item_info_list_return = []
        for item_info in item_info_list:
            item_info_return = {
                "id": item_info[0].id,
                "info": item_info[0].info,
                "type": item_info[0].type,
                "desc": item_info[0].desc,
                "campus": item_info[0].campus,
                "uid": item_info[0].uid,
                "image": item_info[0].image,
                "date": item_info[0].date,
                "place": item_info[0].place,
                "is_claim": item_info[0].is_claim,
                "is_delete": item_info[0].is_delete,
                "phone": item_info[1],
                "username": item_info[2]
            }
            item_info_list_return.append(item_info_return)

        data_content = {
            "total": total,
            "pagenum": pagenum,
            "pagesize": pagesize,
            "item_info_list": item_info_list_return
        }

        data = {
            "data": marshal(data_content, item_info_list_fields),
            "meta": {
                "status": 200,
                "msg": "获取成功"
            }
        }
        return data


class ItemNumberResource(Resource):
    def get(self):
        number = ItemInfo.query.filter(ItemInfo.is_delete == False).count()
        data = {
            "data": {
                "number": number
            },
            "meta": {
                "status": 200,
                "msg": '获取成功'
            }
        }
        return data


class ItemTypeNumberResource(Resource):
    def get(self):
        type_list = session.query(ItemType.type).order_by(ItemType.id.desc()).all()
        data_return = []
        for type in type_list:
            print(type[0])
            single = {
                "name": type[0],
                "value": session.query(ItemInfo).filter(ItemInfo.type==type[0]).count()
            }
            data_return.append(single)
        return {
            "data": data_return,
            "meta": {
                "status": 200,
                "msg": "获取成功"
            }

        }
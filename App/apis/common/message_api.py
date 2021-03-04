import datetime

from flask import g
from flask_restful import Resource, reqparse, fields, marshal

from App.models.message_model import Message
from App.models.user_model import User
from App.settings import session
from App.utils import user_login_required, error_info, admin_login_required

parse_post = reqparse.RequestParser()
parse_post.add_argument('content', type=str, required=True, help='请提供内容')
parse_post.add_argument('receiveId', type=str, required=True, help='请提供收件人id')

parse = reqparse.RequestParser()
parse.add_argument('id', type=str, required=True, help='请提供消息编号')

message_fields = {
    "id": fields.String,
    "sendId": fields.String,
    "content": fields.String,
    "status": fields.String,
    "date": fields.DateTime,
}

message_list_fields = {
    "message_list": fields.List(fields.Nested(message_fields))
}


class MessageResource(Resource):
    @admin_login_required
    def post(self):
        args = parse_post.parse_args()
        receiveId = args.get('receiveId')

        message = Message()

        if receiveId == 'all':
            users = session.query(User.id).filter(User.is_delete == False).all()
            for user in users:
                msg = Message()
                msg.content = args.get('content')
                msg.sendId = g.user.id
                msg.date = datetime.datetime.now()
                msg.receiveId = user[0]
                msg.id = msg.receiveId + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                if not msg.save():
                    return error_info(400, '操作失败')
                message = msg
        else:
            message.content = args.get('content')
            message.sendId = g.user.id
            message.date = datetime.datetime.now()
            user = session.query(User).filter(User.is_delete == False, User.id == receiveId).first()
            if not user:
                return error_info(400, '用户不存在')

            message.receiveId = receiveId
            message.id = message.receiveId + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not message.save():
                return error_info(400, '操作失败')

        data = {
            "data": marshal(message, message_fields),
            "meta": {
                "status": 201,
                "msg": "消息发送成功"
            }
        }
        return data

    @user_login_required
    def get(self):
        message = Message.query.filter(Message.receiveId == g.user.id, Message.status!='2').order_by(Message.date.desc()).all()
        data_content = {
            "message_list": message
        }

        data = {
            "data": marshal(data_content, message_list_fields),
            "meta": {
                "status": 200,
                "msg": "消息列表获取成功"
            }
        }

        return data

    @user_login_required
    def put(self):
        args = parse.parse_args()
        id = args.get('id')

        message = Message.query.filter(Message.id == id, Message.receiveId == g.user.id, Message.status=='0').first()
        if not message:
            return error_info(400, '修改状态失败')

        message.status = '1'
        message.save()

        data = {
            "data": {
                "id": message.id,
                "status": message.status
            },
            "meta": {
                "status": 201,
                "msg": "修改状态成功"
            }
        }

        return data

    @user_login_required
    def delete(self):
        args = parse.parse_args()
        id = args.get('id')

        message = Message.query.filter(Message.id == id, Message.receiveId == g.user.id).first()
        if not message:
            return error_info(400, '删除失败')

        message.status = '2'
        message.save()

        data = {
            "data": {
                "id": message.id,
                "status": message.status
            },
            "meta": {
                "status": 204,
                "msg": "删除成功"
            }
        }

        return data
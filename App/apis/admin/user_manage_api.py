from flask_restful import Resource, reqparse, marshal, fields
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from App.models.user_model import User
from App.utils import error_info, admin_login_required

parse = reqparse.RequestParser()
parse.add_argument("type", type=str, required=True, help="请提供操作参数")
parse.add_argument("id", type=str, required=True, help="请提供学号")

parse_query = reqparse.RequestParser()
parse_query.add_argument("query", type=str, required=True, help="请提供query参数")
parse_query.add_argument("pagenum", type=int, required=True, help="请提供pagenum参数")
parse_query.add_argument("pagesize", type=int, required=True, help="请提供pagesize参数")

single_user_fields = {
    "id": fields.String,
    "username": fields.String,
    "name": fields.String,
    "phone": fields.String,
    "status": fields.Boolean
}

multi_user_fields = {
    "total": fields.Integer,
    "pagenum": fields.Integer,
    "pagesize": fields.Integer,
    "users": fields.List(fields.Nested(single_user_fields)),
}


class UserManageResource(Resource):
    @admin_login_required
    def get(self):
        args = parse_query.parse_args()
        query = args.get("query")
        pagenum = args.get("pagenum")
        pagesize = args.get("pagesize")

        if query == "":
            users = User.query.filter(User.is_delete == False).offset(pagesize* (pagenum-1)).limit(pagesize)
            data_content = {
                "total": User.query.filter(User.is_delete == False).count(),
                "pagenum": pagenum,
                "pagesize": pagesize,
                "users": users,
            }

        else:
            users = User.query.filter(User.is_delete == False, or_(User.id == query, User.username.like("%"+query+"%"), User.name.like("%"+query+"%"))).offset(pagesize* (pagenum-1)).limit(pagesize)
            data_content = {
                "total":  User.query.filter(User.is_delete == False, or_(User.id == query, User.username.like("%"+query+"%"), User.name.like("%"+query+"%"))).count(),
                "pagenum": pagenum,
                "pagesize": pagesize,
                "users": users,
            }
        data = {
            "data": marshal(data_content, multi_user_fields),
            "meta": {
                "status": 200,
                "msg": "获取成功"
            }
        }
        return data

    @admin_login_required
    def put(self):
        args = parse.parse_args()
        type = args.get('type')
        id = args.get('id')

        if type == 'status':
            user = User.query.filter(User.id == id).first()
            if not user:
                return error_info(400, '该用户不存在')
            user.status = not user.status
            user.save()

            data = {
                "data": {
                    "id": user.id,
                    "status": user.status
                },
                "meta": {
                    "status": 201,
                    "msg": "状态更改成功"
                }
            }
            return data

        elif type == 'password':
            user = User.query.filter(User.id == id).first()
            if not user:
                return error_info(400, '该用户不存在')
            user.password = generate_password_hash('123123')
            user.save()

            data = {
                "data": {
                    "id": user.id,
                    "status": user.status
                },
                "meta": {
                    "status": 201,
                    "msg": "密码重置成功"
                }
            }
            return data

        else:
            return error_info(400, "参数错误")
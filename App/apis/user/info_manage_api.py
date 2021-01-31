from flask import g
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from App.ext import cache
from App.models.user_model import User
from App.utils import user_login_required, error_info, generate_user_token

parse = reqparse.RequestParser()
parse.add_argument('username', type=str)
parse.add_argument('name', type=str)
parse.add_argument('phone', type=str)
parse.add_argument('password', type=str)


class InfoManageResource(Resource):
    @user_login_required
    def put(self):
        args = parse.parse_args()
        if args.get('username'):
            if User.query.filter(User.username == args.get('username')).first():
                return error_info(400, "该用户名已存在")
            g.user.username = args.get('username')
        if args.get('name'):
            g.user.name = args.get('name')
        if args.get('phone'):
            g.user.phone = args.get('phone')
        if args.get('password'):
            g.user.password = generate_password_hash(args.get('password'))
        g.user.save()

        token = generate_user_token()
        cache.set(token, g.user.id, timeout=60 * 60 * 24 * 7)

        data = {
            "data": {
                "id": g.user.id,
                "username": g.user.username,
                "phone": g.user.phone,
                "status": g.user.status,
                "token": token
            },
            "meta": {
                "status": 201,
                "msg": "信息更改成功"
            }
        }
        return data


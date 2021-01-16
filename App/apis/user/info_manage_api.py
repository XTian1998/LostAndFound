from flask import g
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from App.utils import user_login_required

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
            g.user.username = args.get('username')
        if args.get('name'):
            g.user.name = args.get('name')
        if args.get('phone'):
            g.user.phone = args.get('phone')
        if args.get('password'):
            g.user.password = generate_password_hash(args.get('password'))
        g.user.save()
        data = {
            "data": {
                "id": g.user.id,
                "username": g.user.username,
                "name": g.user.name,
                "phone": g.user.phone,
                "status": g.user.status
            },
            "meta": {
                "status": 200,
                "msg": "信息更改成功"
            }
        }
        return data


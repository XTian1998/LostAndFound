import datetime

from flask import g
from flask_restful import Resource, reqparse, marshal, fields

from App.models.notice_model import Notice
from App.utils import user_login_required, error_info

parse = reqparse.RequestParser()
parse.add_argument('type', type=str, required=True, help="请提供类型")
parse.add_argument('content', type=str, required=True, help="请提供内容")

parse_del = reqparse.RequestParser()
parse_del.add_argument('id', type=str, required=True, help="请提供编号")

parse_query = reqparse.RequestParser()
parse_query.add_argument("pagenum", type=int, required=True, help="请提供pagenum参数")
parse_query.add_argument("pagesize", type=int, required=True, help="请提供pagesize参数")
parse_query.add_argument('type', type=str, help="请提供类型")
parse_query.add_argument('creator', type=str, help="请提供用户id")

notice_fields = {
    'id': fields.String,
    'type': fields.String,
    'title': fields.String,
    'content': fields.String,
    'creator': fields.String,
    'date': fields.DateTime,
    'is_delete': fields.Boolean
}

notice_list_fields = {
    "total": fields.Integer,
    "pagenum": fields.Integer,
    "pagesize": fields.Integer,
    "notice_list": fields.List(fields.Nested(notice_fields))
}


class UserNoticeResource(Resource):

    @user_login_required
    def post(self):
        args = parse.parse_args()
        type = args.get('type')

        if type != '用户留言':
            return error_info(400, '参数错误')

        notice = Notice()
        notice.type = type
        notice.content = args.get('content')
        notice.creator = g.user.id
        notice.date = datetime.datetime.now()
        notice.id = g.user.id + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        if not notice.save():
            return error_info(400, '操作失败')

        data = {
            "data": marshal(notice, notice_fields),
            "meta": {
                "status": 201,
                "msg": "发布成功"
            }
        }

        return data

    @user_login_required
    def delete(self):
        args = parse_del.parse_args()
        notice = Notice.query.filter(Notice.creator == g.user.id, Notice.id == args.get('id'), Notice.is_delete == False).first()
        if not notice:
            return error_info(400, '操作失败')

        notice.is_delete = True
        notice.save()
        data = {
            "data": marshal(notice, notice_fields),
            "meta": {
                "status": 204,
                "msg": "删除成功"
            }
        }

        return data

    def get(self):
        args = parse_query.parse_args()
        pagenum = args.get('pagenum')
        pagesize = args.get('pagesize')
        notice_list = Notice.query.filter(Notice.is_delete == False, Notice.type != '管理员公告')
        if args.get('type'):
            notice_list = notice_list.filter(Notice.type == args.get('type'))
        if args.get('creator'):
            notice_list = notice_list.filter(Notice.creator == args.get('creator'))

        data_content = {
            "total": notice_list.count(),
            "pagenum": pagenum,
            "pagesize": pagesize,
            "notice_list": notice_list.order_by(Notice.date.desc()).offset(pagesize* (pagenum-1)).limit(pagesize)
        }

        data = {
            "data": marshal(data_content, notice_list_fields),
            "meta": {
                "status": 200,
                "msg": "获取成功"
            }
        }
        return data
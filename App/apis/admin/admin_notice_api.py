import datetime

from flask import g
from flask_restful import Resource, reqparse, fields, marshal

from App.models.notice_model import Notice
from App.utils import admin_login_required, error_info

parse_edit = reqparse.RequestParser()
parse_edit.add_argument('title', type=str, required=True, help="请提供标题")
parse_edit.add_argument('content', type=str, help="请提供内容")
parse_edit.add_argument('id', type=str, required=True, help="请提供公告编号")


parse = reqparse.RequestParser()
parse.add_argument('title', type=str, required=True, help="请提供标题")
parse.add_argument('content', type=str, help="请提供内容")

parse_del = reqparse.RequestParser()
parse_del.add_argument('id', type=str, required=True, help="请提供公告编号")

admin_notice_fields = {
    'id': fields.String,
    'type': fields.String,
    'title': fields.String,
    'content': fields.String,
    'creator': fields.String,
    'date': fields.DateTime,
    'is_delete': fields.Boolean
}

admin_notice_list_fields = {
    "admin_notice_list": fields.List(fields.Nested(admin_notice_fields))
}


class AdMinNoticeResource(Resource):
    @admin_login_required
    def post(self):
        args = parse.parse_args()

        admin_notice = Notice()
        admin_notice.type = "管理员公告"
        admin_notice.title= args.get('title')
        admin_notice.content = args.get('content')
        admin_notice.creator = g.user.id
        admin_notice.date = datetime.datetime.now()
        admin_notice.id = g.user.id + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        if not admin_notice.save():
            return error_info(400, '操作失败')

        data = {
            "data": marshal(admin_notice, admin_notice_fields),
            "meta": {
                "status": 201,
                "msg": "发布成功"
            }
        }

        return data

    @admin_login_required
    def put(self):
        args = parse_edit.parse_args()
        notice = Notice.query.filter(Notice.creator == g.user.id, Notice.id == args.get('id'),
                                Notice.is_delete == False).first()
        if not notice:
            return error_info(400, '操作失败')
        notice.title = args.get('title')
        notice.content = args.get('content')
        notice.creator = g.user.id
        notice.date = datetime.datetime.now()
        notice.id = g.user.id + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if not notice.save():
            return error_info(400, '操作失败')

        data = {
            "data": marshal(notice, admin_notice_fields),
            "meta": {
                "status": 201,
                "msg": "发布成功"
            }
        }

        return data

    @admin_login_required
    def delete(self):
        args = parse_del.parse_args()
        notice = Notice.query.filter(Notice.creator == g.user.id, Notice.id == args.get('id'), Notice.is_delete == False).first()
        if not notice:
            return error_info(400, '操作失败')

        notice.is_delete = True
        notice.save()
        data = {
            "data": marshal(notice, admin_notice_fields),
            "meta": {
                "status": 204,
                "msg": "删除成功"
            }
        }

        return data

    def get(self):
        notice_list = Notice.query.filter(Notice.type == '管理员公告', Notice.is_delete == False).order_by(Notice.date.desc()).all()

        data_content = {
            "admin_notice_list": notice_list
        }
        data = {
            "data": marshal(data_content, admin_notice_list_fields),
            "meta": {
                "status": 200,
                "msg": "获取成功"
            }
        }

        return data

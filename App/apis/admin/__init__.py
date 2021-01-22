from flask_restful import Api

from App.apis.admin.admin_notice_api import AdMinNoticeResource
from App.apis.admin.admin_sign_api import AdminResource
from App.apis.admin.user_manage_api import UserManageResource

admin_api = Api(prefix="/admin")

admin_api.add_resource(AdminResource, '/')
admin_api.add_resource(UserManageResource, '/user_manage/')
admin_api.add_resource(AdMinNoticeResource, '/notice/')

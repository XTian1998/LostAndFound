from flask_restful import Api

from App.apis.user.info_manage_api import InfoManageResource
from App.apis.user.user_sign_api import UserResource

user_api = Api(prefix="/user")

user_api.add_resource(UserResource, '/')
user_api.add_resource(InfoManageResource, '/info_manage/')

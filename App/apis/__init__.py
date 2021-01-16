from App.apis.admin import admin_api
from App.apis.common import common_api
from App.apis.user import user_api


def init_api(app):
    admin_api.init_app(app)
    user_api.init_app(app)
    common_api.init_app(app)


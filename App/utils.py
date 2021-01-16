import uuid

from flask import request, g

from App.ext import cache
from App.models.admin_model import Admin
from App.models.user_model import User
from App.settings import UPLOADS_DIR, FILE_PATH_PREFIX

USER = "user"
ADMIN = "admin"


def error_info(status, msg):
    return {
                "data": None,
                "meta": {
                    "status": status,
                    "msg": msg
                }
            }


def generate_token(prefix):
    token = prefix + uuid.uuid4().hex
    return token


def generate_admin_token():
    return generate_token(prefix=ADMIN)


def generate_user_token():
    return generate_token(prefix=USER)


def get_admin(user_id):

    if not user_id:
        return None

    user = Admin.query.filter(Admin.id == user_id).first()
    if user:
        return user
    return None


def get_user(user_id):

    if not user_id:
        return None

    user = User.query.filter(User.id == user_id).first()
    if user:
        return user
    return None


def admin_login_required(fun):

    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return error_info(401, "请先登录")

        if not token.startswith(ADMIN):
            return error_info(401, "没有权限")

        user_id = cache.get(token)

        if not user_id:
            return error_info(401, "用户不存在")

        user = get_admin(user_id)

        if not user:
            return error_info(401, "用户不存在")

        g.user = user
        g.auth = token
        return fun(*args, **kwargs)
    return wrapper


def user_login_required(fun):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return error_info(401, "请先登录")

        if not token.startswith(USER):
            return error_info(401, "没有权限")

        user_id = cache.get(token)

        if not user_id:
            return error_info(401, "用户不存在")

        user = get_user(user_id)

        if not user:
            return error_info(401, "用户不存在")

        g.user = user
        g.auth = token
        return fun(*args, **kwargs)
    return wrapper


def filename_transfer(filename):
    ext_name = filename.rsplit(".")[1]

    new_filename = uuid.uuid4().hex + '.' + ext_name

    save_path = UPLOADS_DIR + "/" +new_filename

    upload_path = FILE_PATH_PREFIX + "/" + new_filename

    return save_path, upload_path
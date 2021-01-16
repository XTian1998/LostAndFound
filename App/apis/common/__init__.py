from flask_restful import Api

from App.apis.common.item_image_uploads_api import ItemImageResource
from App.apis.common.item_info_api import ItemInfoResource
from App.apis.common.item_type_api import ItemTypeResource

common_api = Api()

common_api.add_resource(ItemTypeResource, '/type/')
common_api.add_resource(ItemImageResource, '/uploads/')
common_api.add_resource(ItemInfoResource, '/iteminfo/')

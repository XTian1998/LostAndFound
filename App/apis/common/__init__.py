from flask_restful import Api, Resource

from App.apis.common.item_image_uploads_api import ItemImageResource
from App.apis.common.item_info_api import ItemInfoResource, ItemNumberResource
from App.apis.common.item_type_api import ItemTypeResource
from App.apis.common.message_api import MessageResource

common_api = Api()


class HelloResource(Resource):
    def get(self):
        return 'hello'


common_api.add_resource(HelloResource, '/')
common_api.add_resource(ItemTypeResource, '/type/')
common_api.add_resource(ItemImageResource, '/uploads/')
common_api.add_resource(ItemInfoResource, '/iteminfo/')
common_api.add_resource(MessageResource, '/message/')
common_api.add_resource(ItemNumberResource, '/iteminfo/number/')


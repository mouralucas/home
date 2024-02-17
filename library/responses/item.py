from base.responses import DefaultSuccessResponse
from base.serializers import CustomSerializer
from library.serializers.item import ItemSerializer


class ItemPostResponse(DefaultSuccessResponse, CustomSerializer):
    item = ItemSerializer()

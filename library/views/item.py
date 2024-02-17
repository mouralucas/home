from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import service.library.author
import service.library.library
from base.responses import InvalidRequestError, NotImplementedResponse
from library.requests.item import ItemPostRequest, ItemGetRequest
from library.responses.item import ItemPostResponse
from service.security.security import IsAuthenticated


class Item(APIView):
    permission_classes = [IsAuthenticated]

    """
    :Nome da classe/função: Item
    :descrição: View to handle any kind of itens in library (books, mangas, etc)
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    @extend_schema(summary='Get items',
                   parameters=[ItemGetRequest], responses={200: None, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = ItemGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        item_id = data.validated_data.get('itemId')
        item_type = data.validated_data.get('itemType')
        is_unique = data.validated_data.get('isUnique')
        user = self.request.user.id

        response = service.library.library.Library(owner=user, item_id=item_id, item_type=item_type).get_item(is_unique=is_unique)

        return Response(response)

    @extend_schema(summary='Create a new item', description='Create a new item',
                   request=ItemPostRequest, responses={200: ItemPostResponse, 400: InvalidRequestError})
    def post(self, *args, **kwargs):
        data = ItemPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.id

        response = service.library.library.Library(item_id=data.validated_data.get('itemId'), owner=user).set_item(data=data, request=self.request)

        return Response(response, status=response['statusCode'])

    @extend_schema(summary='Update an existing item', description='Update an existing item(Not implemented)')
    def put(self, *args, **kwargs):
        data = ItemPostRequest(data=self.request)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)

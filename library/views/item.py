from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import service.library.author
import service.library.library
from library.serializers import ItemGetSerializer, ItemPostSerializer
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

    def get(self, *args, **kwargs):
        data = ItemGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        item_id = data.validated_data.get('itemId')
        item_type = data.validated_data.get('itemType')
        is_unique = data.validated_data.get('isUnique')
        user = self.request.user.id

        response = service.library.library.Library(owner=user, item_id=item_id, item_type=item_type).get_item(is_unique=is_unique)

        return Response(response)

    def post(self, *args, **kwargs):
        data = ItemPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        user = self.request.user.id

        response = service.library.library.Library(item_id=data.validated_data.get('itemId'), owner=user).set_item(data=data, request=self.request)

        return JsonResponse(response, safe=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ItemGetSerializer
        elif self.request.method == 'POST':
            return ItemPostSerializer

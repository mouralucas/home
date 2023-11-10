from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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

    @swagger_auto_schema(
        operation_description='Returns all order based on parameters\nIf orderId is passed, returns a single result in \'orders\' object',
        manual_parameters=[
            openapi.Parameter(
                name='itemId', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description=_('Id do item'), required=False,
            ),
            openapi.Parameter(
                name='itemType', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description=_('Tipo do item a ser buscado'), required=True,
            ),
            openapi.Parameter(
                name='isUnique', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description=_('Indica se o retorno deve ser um objeto ou lista'), required=False, default=False
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'qtd': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'single_result': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'items': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'itemId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'title': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'subtitle': openapi.Schema(type=openapi.TYPE_STRING),
                                    'titleOriginal': openapi.Schema(type=openapi.TYPE_STRING),
                                    'subtitleOriginal': openapi.Schema(type=openapi.TYPE_STRING),
                                    'mainAuthorName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'mainAuthorId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'serieName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'serieId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'collectionName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'collectionId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'publisherName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'publisherId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'volume': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'edition': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'publishedAt': openapi.Schema(type=openapi.TYPE_STRING),
                                    'originalPublishedAt': openapi.Schema(type=openapi.TYPE_STRING),
                                    'lastStatusName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'lastStatusId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'lastStatusAt': openapi.Schema(type=openapi.TYPE_STRING),
                                    'itemType': openapi.Schema(type=openapi.TYPE_STRING),
                                    'itemFormatId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'languageName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'languageId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'dimensions': openapi.Schema(type=openapi.TYPE_STRING),
                                    'height': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'width': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'thickness': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'summary': openapi.Schema(type=openapi.TYPE_STRING),
                                    'isbn': openapi.Schema(type=openapi.TYPE_STRING),
                                    'isbnFormatted': openapi.Schema(type=openapi.TYPE_STRING),
                                    'isbn10': openapi.Schema(type=openapi.TYPE_STRING),
                                    'isbnFormatted10': openapi.Schema(type=openapi.TYPE_STRING),
                                    'coverPrice': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'paidPrice': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'createdAt': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'lastEditedAt': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            ),
                        ),
                    },
                    required=['field1'],
                ),
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Acesso proibido",
            ),
        },
    )
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
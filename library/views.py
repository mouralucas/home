import json

from django.http import JsonResponse
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.author.author
import service.core.core
import service.library.library
from service.security.security import IsAuthenticated
from library.serializers import ItemGetSerializer, ItemPostSerializer
from django.utils.translation import gettext_lazy as _


class ItemAuthor(View):
    def get(self, *args, **kwargs):
        book_id = self.request.GET.get('item_id')

        response = service.library.library.Library(item_id=book_id).get_item_authors()

        return JsonResponse(response, safe=False)


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
        validators = ItemGetSerializer(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        item_id = validators.validated_data.get('itemId')
        item_type = validators.validated_data.get('itemType')
        is_unique = validators.validated_data.get('isUnique')
        user = self.request.user.id

        response = service.library.library.Library(owner=user, item_id=item_id, item_type=item_type).get_item(is_unique=is_unique)

        return Response(response)

    def post(self, *args, **kwargs):
        data = ItemPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        item_id = self.request.POST.get('item_id') if self.request.POST.get('item_id') != 'null' else None
        status = self.request.POST.get('last_status_id')
        dat_last_status = self.request.POST.get('dat_last_status')
        main_author_id = self.request.POST.get('main_author_id') if self.request.POST.get('main_author') != '0' else None
        authors_id = json.loads(self.request.POST.get('authors_id')) if self.request.POST.get('authors_id') else None
        title = self.request.POST.get('title') if self.request.POST.get('title') not in ('null', None, '', '0') else None
        subtitle = self.request.POST.get('subtitle') if self.request.POST.get('subtitle') not in ('null', None, '', '0') else None
        title_original = self.request.POST.get('title_original') if self.request.POST.get('title_original') not in ('null', None, '', '0') else None
        subtitle_original = self.request.POST.get('subtitle_original') if self.request.POST.get('subtitle_original') not in ('null', None, '', '0') else None
        isbn_formatted = self.request.POST.get('isbn_formatted')
        isbn_10_formatted = self.request.POST.get('isbn10_formatted')
        item_type = self.request.POST.get('itemType')
        pages = self.request.POST.get('pages')
        volume = self.request.POST.get('volume')
        edition = self.request.POST.get('edition')
        dat_published = self.request.POST.get('dat_published')
        dat_published_original = self.request.POST.get('dat_published_original')
        serie_id = self.request.POST.get('serie_id')
        collection_id = self.request.POST.get('collection_id')
        publisher_id = self.request.POST.get('publisher_id')
        item_format = self.request.POST.get('itemFormatId')
        language_id = self.request.POST.get('language_id')
        cover_price = self.request.POST.get('cover_price')
        payed_price = self.request.POST.get('payed_price')
        dimensions = self.request.POST.get('dimensions')
        height = self.request.POST.get('height') if self.request.POST.get('height') not in ('null', None, '', '0') else None
        width = self.request.POST.get('width') if self.request.POST.get('width') not in ('null', None, '', '0') else None
        thickness = self.request.POST.get('thickness') if self.request.POST.get('thickness') not in ('null', None, '', '0') else None
        summary = self.request.POST.get('summary')
        user = self.request.user.id

        response = service.library.library.Library(item_id=item_id, owner=user).set_item(data=data, request=self.request)

        response = {}

        return JsonResponse(response, safe=False)


class Author(APIView):
    permission_classes = [IsAuthenticated]
    """
    :Nome da classe/função: Author
    :descrição: View to handle informatiom about authors
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        """
        :Nome da classe/função: Author get
        :descrição: View to handle informatiom about authors
        :Criação: Lucas Penha de Moura - 20/02/2022
        :Edições:
        :return
        """
        is_tradutor = True if self.request.GET.get('is_tradutor') else False

        response = service.author.author.Author().get_author(is_translator=is_tradutor)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        author_id = self.request.POST.get('author_id')
        nm_full = self.request.POST.get('nm_full')
        dat_birth = self.request.POST.get('dat_birth')
        description = self.request.POST.get('description')
        is_translator = False
        language_id = self.request.POST.get('language_id')
        country_id = self.request.POST.get('country_id')

        response = service.author.author.Author(author_id=author_id).set_author(nm_full=nm_full, dat_birth=dat_birth,
                                                                                description=description, is_translator=is_translator,
                                                                                language_id=language_id, country_id=country_id,
                                                                                request=self.request)

        return JsonResponse(response, safe=False)


class Status(View):
    permission_classes = [IsAuthenticated]
    """
    :Nome da classe/função: Status
    :descrição: View to handle informatiom about item status
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = service.library.library.Library().get_status(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Type(View):
    permission_classes = [IsAuthenticated]
    """
    :Nome da classe/função: Type
    :descrição: View to handle the different types of items
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = service.library.library.Library().get_types(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Format(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = service.library.library.Library().get_formats()

        return JsonResponse(response, safe=False)


class Serie(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id') if self.request.GET.get('selected_id') != '' else None

        response = service.library.library.Library().get_serie()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        serie_id = self.request.POST.get('serie_id')
        name = self.request.POST.get('name')
        nm_original = self.request.POST.get('nm_original')
        description = self.request.POST.get('description')
        country_id = self.request.POST.get('country_id')

        response = service.library.library.Library().set_serie(serie_id=serie_id, name=name, nm_original=nm_original,
                                                               description=description, country_id=country_id, request=self.request)

        return JsonResponse(response, safe=False)


class Collection(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = service.library.library.Library().get_collection()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        nm_descritivo = self.request.POST.get('nm_descritivo')
        nm_original = self.request.POST.get('nm_original')
        descricao = self.request.POST.get('descricao')
        pais_id = self.request.POST.get('pais_id')

        response = service.library.library.Library().set_serie(name=nm_descritivo, nm_original=nm_original,
                                                               description=descricao, country_id=pais_id, request=self.request)

        return JsonResponse(response, safe=False)


class Publisher(APIView):
    permission_classes = [IsAuthenticated]
    """
    :Nome da classe/função: Publisher
    :descrição: View to handle informatiom about publishers
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', 0)

        response = service.library.library.Library().get_publishers(selected_id=selected_id)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        publisher_id = self.request.POST.get('publisher_id')
        name = self.request.POST.get('name')
        description = self.request.POST.get('description')
        country_id = self.request.POST.get('country_id')
        parent_id = self.request.POST.get('parent_id')

        response = service.library.library.Library().set_publisher(name=name, description=description, country_id=country_id, parent_id=parent_id,
                                                                   publisher_id=publisher_id, request=self.request)

        return Response(response)


class Language(View):
    """
    :Nome da classe/função: Language
    :descrição: View to handle informations about languages_
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = service.core.core.Misc().get_language(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Country(View):
    """
    :Nome da classe/função: Language
    :descrição: View to handle informations about countries
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)

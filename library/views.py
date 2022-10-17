import json

from django.http import JsonResponse
from django.views import View
from BO.security.security import IsAuthenticated
from rest_framework.views import APIView

import BO.author.author
import BO.core.core
import BO.library.library
import util.datetime


class ItemAuthor(View):
    def get(self, *args, **kwargs):
        book_id = self.request.GET.get('item_id')

        response = BO.library.library.Library(item_id=book_id).get_item_authors(is_selected=True)

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

    def get(self, *args, **kwargs):
        item_id = self.request.GET.get('item_id')
        item_type = self.request.GET.get('item_type')
        is_unique = True if self.request.GET.get('is_unique') else False

        response = BO.library.library.Library(item_id=item_id, item_type=item_type).get_item(is_unique=is_unique)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        item_id = self.request.POST.get('item_id') if self.request.POST.get('item_id') != 'null' else None
        status = self.request.POST.get('status')
        dat_status = self.request.POST.get('dat_status')
        main_author_id = self.request.POST.get('main_author_id') if self.request.POST.get('main_author') != '0' else None
        authors_id = json.loads(self.request.POST.get('authors_id')) if self.request.POST.get('authors_id') else None
        title = self.request.POST.get('title')
        subtitle = self.request.POST.get('subtitle')
        title_original = self.request.POST.get('title_original')
        subtitle_original = self.request.POST.get('subtitle_original')
        isbn = self.request.POST.get('isbn')
        isbn_10 = self.request.POST.get('isbn_10')
        type = self.request.POST.get('itemType')
        pages = self.request.POST.get('pages')
        volume = self.request.POST.get('volume')
        edition = self.request.POST.get('edition')
        dat_published = self.request.POST.get('dat_published')
        dat_published_original = self.request.POST.get('dat_published_original')
        serie_id = self.request.POST.get('serie_id')
        collection_id = self.request.POST.get('collection_id')
        publisher_id = self.request.POST.get('publisher_id')
        item_format = self.request.POST.get('format_id')
        language_id = self.request.POST.get('language_id')
        cover_price = self.request.POST.get('cover_price')
        payed_price = self.request.POST.get('payed_price')
        dimensions = self.request.POST.get('dimensions')
        height = self.request.POST.get('height')
        width = self.request.POST.get('width')
        thickness = self.request.POST.get('thickness')
        resumo = self.request.POST.get('resumo')

        response = BO.library.library.Library(item_id=item_id).set_item(main_author_id=main_author_id, authors_id=authors_id, title=title, subtitle=subtitle, title_original=title_original,
                                                                        subtitle_original=subtitle_original, isbn=isbn, isbn_10=isbn_10, type=type,
                                                                        pages=pages, volume=volume, edition=edition, dat_published=dat_published,
                                                                        dat_published_original=dat_published_original, serie_id=serie_id, collection_id=collection_id, publisher=publisher_id,
                                                                        item_format=item_format, language_id=language_id, cover_price=cover_price, payed_price=payed_price,
                                                                        dimensions=dimensions, heigth=height, width=width, thickness=thickness,
                                                                        status=status, dat_status=dat_status, resumo=resumo)

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

        response = BO.author.author.Author().get_author(is_translator=is_tradutor)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        nm_full = self.request.POST.get('nm_full')
        dat_birth = util.datetime.format_data(self.request.POST.get('dat_birth'))
        description = self.request.POST.get('description')
        is_translator = False if self.request.POST.get('is_translator') == 'n' else True
        language_id = self.request.POST.get('language_id')
        country_id = self.request.POST.get('country_id')

        response = BO.author.author.Author().set_author(nm_full=nm_full, dat_birth=dat_birth,
                                                        description=description, is_translator=is_translator,
                                                        language_id=language_id, country_id=country_id,
                                                        request=self.request)

        return JsonResponse(response, safe=False)


class Status(View):
    """
    :Nome da classe/função: Status
    :descrição: View to handle informatiom about item status
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = BO.library.library.Library().get_status(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Type(View):
    """
    :Nome da classe/função: Type
    :descrição: View to handle the different types of items
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = BO.library.library.Library().get_types(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Format(View):
    def get(self, *args, **kwargs):
        response = BO.library.library.Library().get_formats()

        return JsonResponse(response, safe=False)


class Serie(View):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id') if self.request.GET.get('selected_id') != '' else None

        response = BO.library.library.Library().get_series()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        nm_descritivo = self.request.POST.get('nm_descritivo')
        nm_original = self.request.POST.get('nm_original')
        descricao = self.request.POST.get('descricao')
        pais_id = self.request.POST.get('pais_id')

        response = BO.library.library.Library().set_serie(nm_descritivo=nm_descritivo, nm_original=nm_original,
                                                          descricao=descricao, pais_id=pais_id, request=self.request)

        return JsonResponse(response, safe=False)


class Colecao(View):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id') if self.request.GET.get('selected_id') != '' else None

        response = BO.library.library.Library().get_colecoes()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        nm_descritivo = self.request.POST.get('nm_descritivo')
        nm_original = self.request.POST.get('nm_original')
        descricao = self.request.POST.get('descricao')
        pais_id = self.request.POST.get('pais_id')

        response = BO.library.library.Library().set_serie(nm_descritivo=nm_descritivo, nm_original=nm_original,
                                                          descricao=descricao, pais_id=pais_id, request=self.request)

        return JsonResponse(response, safe=False)


class Publisher(View):
    """
    :Nome da classe/função: Publisher
    :descrição: View to handle informatiom about publishers
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', 0)

        response = BO.library.library.Library().get_publishers(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Language(View):
    """
    :Nome da classe/função: Language
    :descrição: View to handle informations about languages
    :Criação: Lucas Penha de Moura - 20/02/2022
    :Edições:
    :return
    """

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id', '')

        response = BO.core.core.Misc().get_language(selected_id=selected_id)

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
        response = BO.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)

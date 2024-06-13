from django.http import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import service.library.author
import service.library.library
from service.security.security import IsAuthenticated


class ItemAuthor(View):
    def get(self, *args, **kwargs):
        book_id = self.request.GET.get('item_id')

        response = service.library.library.Library(item_id=book_id).get_item_authors()

        return JsonResponse(response, safe=False)




class Author(APIView):
    permission_classes = [IsAuthenticated]
    """
    :Nome da classe/função: Author
    :descrição: View to handle information about authors
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

        response = service.library.author.Author().get_author(is_translator=is_tradutor)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        author_id = self.request.POST.get('author_id')
        nm_full = self.request.POST.get('nm_full')
        dat_birth = self.request.POST.get('dat_birth')
        description = self.request.POST.get('description')
        is_translator = False
        language_id = self.request.POST.get('language_id')
        country_id = self.request.POST.get('country_id')

        response = service.library.author.Author(author_id=author_id).set_author(nm_full=nm_full, dat_birth=dat_birth,
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


# class Country(View):
#     """
#     :Nome da classe/função: Language
#     :descrição: View to handle informations about countries
#     :Criação: Lucas Penha de Moura - 20/02/2022
#     :Edições:
#     :return
#     """
#
#     def get(self, *args, **kwargs):
#         response = service.core.core.Misc().get_country()
#
#         return JsonResponse(response, safe=False)

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import util.datetime
from core.serializers import ReferenceGetSerializer, CategoryGetSerializer, CategoryPostSerializer


class Country(APIView):
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)


class Module(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.query_params.get('selected_id')

        response = service.core.core.Misc().get_module(id_selected=selected_id)

        return Response(response, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pass


class Category(APIView):

    @extend_schema(
        description='Get the categories from the selected module.',
        parameters=[CategoryGetSerializer],
        responses={200: None, 201: None, 401: None}

    )
    def get(self, *args, **kwargs):
        data = CategoryGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        show_mode = data.validated_data.get('showMode')
        module = data.validated_data.get('module')

        response = service.core.core.Misc().get_category(show_mode=show_mode, module_id=module)

        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(
        request=CategoryPostSerializer,
        responses={501: None}
    )
    def post(self, *args, **kwargs):
        """
                Not implemented.

                This endpoint was not implemented yet.
                ---
                """
        return Response({'success': False, 'message': 'This endpoint was not implemented yet'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class Period(APIView):
    def get(self, *args, **kwargs):
        data = ReferenceGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        s_month = data.validated_data.get('sMonth')
        s_year = data.validated_data.get('sYear')
        e_month = data.validated_data.get('eMonth')
        e_year = data.validated_data.get('eYear')

        response = util.datetime.DateTime().list_period(s_month=s_month, s_year=s_year,
                                                        e_month=e_month, e_year=e_year)

        return Response(response, status=200)


class Status(APIView):
    def get(self, *args, **kwargs):
        status_type = self.request.GET.get('status_type')

        response = service.core.core.Misc().get_status(status_type=status_type)

        return JsonResponse(response, safe=False)


class State(APIView):
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_states()

        return JsonResponse(response, safe=False)


class Version(APIView):
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_version()

        return Response(response, status=status.HTTP_200_OK)


# class Swagger(SpectacularSwaggerView):
#     authentication_classes = []
#
#
# class SwaggerSchema(SpectacularAPIView):
#     authentication_classes = []

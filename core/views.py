from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
import service.core.core
import util.datetime
from core.serializers import ReferenceGetSerializer


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
    @swagger_auto_schema(
        operation_description='Returns all order based on parameters\nIf orderId is passed, returns a single result in \'orders\' object',
        manual_parameters=[
            openapi.Parameter(
                name='showMode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description=_('Modo de apresentação (all, children, parent)'), required=True,
            ),
            openapi.Parameter(
                name='module', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description=_('Modulo da categoria'), required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'statusCode': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'categories': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'categoryId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'fatherId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'fatherName': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            ),
                        ),
                    },
                ),
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Acesso proibido",
            ),
        },
    )
    def get(self, *args, **kwargs):
        show_mode = self.request.query_params.get('show_mode')
        module = self.request.query_params.get('module')

        response = service.core.core.Misc().get_category(show_mode=show_mode, module_id=module)

        return Response(response, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pass


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

from django.http import JsonResponse
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import util.datetime
from base.responses import NotImplementedResponse, InvalidRequestError
from core.requests import ReferenceGetRequest, CategoryGetRequest, CategoryPostRequest, StatusGetRequest
from core.responses import CategoryGetResponse, CountryPostResponse


class Country(APIView):
    @extend_schema(summary='Get all countries', description='Get all countries',
                   parameters=[], responses={200: CountryPostResponse})
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)


class Module(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.query_params.get('selected_id')

        response = service.core.core.Misc().get_module(id_selected=selected_id)

        return Response(response, status=response['statusCode'])


class Category(APIView):

    @extend_schema(summary='Get all categories by module', description='Get the categories from the selected module.',
                   parameters=[CategoryGetRequest], responses={200: CategoryGetResponse, 401: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = CategoryGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        show_mode = data.validated_data.get('showMode')
        module = data.validated_data.get('module')

        response = service.core.core.Misc().get_category(show_mode=show_mode, module_id=module)

        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(summary='', description='Not yet implemented',
                   request=CategoryPostRequest, responses={501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)


class Period(APIView):
    def get(self, *args, **kwargs):
        data = ReferenceGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        s_month = data.validated_data.get('sMonth')
        s_year = data.validated_data.get('sYear')
        e_month = data.validated_data.get('eMonth')
        e_year = data.validated_data.get('eYear')

        response = util.datetime.list_period(s_month=s_month, s_year=s_year,
                                             e_month=e_month, e_year=e_year)

        return Response(response, status=200)


class Status(APIView):
    @extend_schema(summary='Get the list of status by type',
                   parameters=[StatusGetRequest], responses={200: None})
    def get(self, *args, **kwargs):
        data = StatusGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        status_type = data.validated_data.get('statusType')

        response = service.core.core.Misc().get_status(status_type=status_type)

        return Response(response, status=response['statusCode'])


class State(APIView):
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_states()

        return JsonResponse(response, safe=False)


class Version(APIView):
    @extend_schema(summary='Get the current version od the system', parameters=[], responses={200: None})
    def get(self, *args, **kwargs):
        response = service.core.core.Misc().get_version()

        return Response(response, status=status.HTTP_200_OK)


class Swagger(SpectacularSwaggerView):

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):

        list_schemas = [
            {
                'name': 'Geral',
                'schema': 'schema'
            },
            {
                'name': 'Finance',
                'schema': 'schema-finance'
            },
            {
                'name': 'Library',
                'schema': 'schema-library'
            },
            {
                'name': 'User',
                'schema': 'schema-user'
            },
            {
                'name': 'Core',
                'schema': 'schema-core'
            }
        ]

        return Response(
            data={
                'title': self.title,
                'swagger_ui_css': self._swagger_ui_resource('swagger-ui.css'),
                'swagger_ui_bundle': self._swagger_ui_resource('swagger-ui-bundle.js'),
                'swagger_ui_standalone': self._swagger_ui_resource('swagger-ui-standalone-preset.js'),
                'favicon_href': self._swagger_ui_favicon(),
                'schema_url': self._get_schema_url(request),
                'settings': self._dump(spectacular_settings.SWAGGER_UI_SETTINGS),
                'oauth2_config': self._dump(spectacular_settings.SWAGGER_UI_OAUTH2_CONFIG),
                'template_name_js': self.template_name_js,
                'csrf_header_name': self._get_csrf_header_name(),
                'schema_auth_names': self._dump(self._get_schema_auth_names()),
                'list_schemas': list_schemas,
            },
            template_name=self.template_name,
        )

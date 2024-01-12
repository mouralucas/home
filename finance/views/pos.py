from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import Response, APIView

from base.responses import NotImplementedResponse, InvalidRequestError
from finance.requests.pos import AvailableProvidersGetRequest, StatementPostRequest
from service.finance.pos import PointOfSales


class ImportStatement(APIView):
    @extend_schema(summary='Import data from POS statement', description='Not yet implemented',
                   request=StatementPostRequest, responses={200: None, 400: InvalidRequestError, 501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        data = StatementPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        file = data.validated_data.get('file')
        period = data.validated_data.get('period')

        response = PointOfSales().import_statement(file=file)

        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)


class Providers(APIView):
    @extend_schema(summary='Get available POS providers', description='Not implemented yet',
                   parameters=[AvailableProvidersGetRequest], responses={200: None, 501: NotImplementedResponse})
    def get(self, *args, **kwargs):
        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)

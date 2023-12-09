from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.core
import service.finance.finance
import util.datetime
from finance.serializers.core import ExpenseGetSerializer
from service.security.security import IsAuthenticated


class Summary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        # TODO: add serializer
        period = self.request.query_params.get('period', util.datetime.DateTime().current_period())
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_summary()

        return Response(response, status=status.HTTP_200_OK)


class Currency(APIView):
    @swagger_auto_schema(
        operation_description='Returns all available currencies',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'statusCode': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'currencies': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'currencyId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'symbol': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            ),
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, *args, **kwargs):
        response = service.finance.core.Core().get_currency()

        return Response(response, status=status.HTTP_200_OK)


class CashFlow(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.core.Core().get_cash_flow()

        return Response(response, status=response['statusCode'])


class TransactionByCategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """
        :Name: TransactionsByCategoryGroup - GET
        :Description: Get the list of transactions by category
        :Created by: Lucas Penha de Moura - 15/10/2023
        :Edited by:
        """
        data = ExpenseGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        period = data.validated_data.get('period')
        category_id = data.validated_data.get('categoryId')

        response = service.finance.core.Core(category_id=category_id, period=period).get_category_transactions_list()

        return Response(response, status=200)


class TransactionsByCategoryAggregated(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """
        :Name: TransactionsByCategoryGroup - GET
        :Description: Get the aggregated transactions by category
        :Created by: Lucas Penha de Moura - 17/10/2023
        :Edited by:
        """
        period = self.request.GET.get('period')
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_category_transactions_aggregated()

        return Response(response)

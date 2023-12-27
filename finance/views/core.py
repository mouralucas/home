from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.core
import service.finance.finance
import util.datetime
from finance.requests.core import TransactionByCategoryListGetSerializer, TransactionsByCategoryAggregatedGetSerializer
from service.security.security import IsAuthenticated


class Bank(APIView):
    @extend_schema(summary='Get the available banks', parameters=[], responses={200:None})
    def get(self, *args, **kwargs):
        bank = service.finance.finance.Finance().get_bank()

        return Response(bank)


class Summary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        # TODO: add serializer
        period = self.request.query_params.get('period', util.datetime.DateTime().current_period())
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_summary()

        return Response(response, status=status.HTTP_200_OK)


class Currency(APIView):
    serializer_class = None

    @extend_schema(summary='Get all available currencies.', responses={200: None})
    def get(self, *args, **kwargs):
        response = service.finance.core.Core().get_currency()

        return Response(response, status=response['statusCode'])


class CashFlow(APIView):
    serializer_class = None

    @extend_schema(summary='Get available cash flow values', responses={200: None})
    def get(self, *args, **kwargs):
        response = service.finance.core.Core().get_cash_flow()

        return Response(response, status=response['statusCode'])


class TransactionByCategoryList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the list of transactions by category', parameters=[TransactionByCategoryListGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        """
        :Name: TransactionsByCategoryGroup - GET
        :Description: Get the list of transactions by category
        :Created by: Lucas Penha de Moura - 15/10/2023
        :Edited by:
        """
        data = TransactionByCategoryListGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        period = data.validated_data.get('period')
        category_id = data.validated_data.get('categoryId')

        response = service.finance.core.Core(category_id=category_id, period=period).get_category_transactions_list()

        return Response(response, status=200)


class TransactionsByCategoryAggregated(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the aggregated transactions by category', parameters=[TransactionsByCategoryAggregatedGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        """
        :Name: TransactionsByCategoryGroup - GET
        :Description: Get the aggregated transactions by category
        :Created by: Lucas Penha de Moura - 17/10/2023
        :Edited by:
        """
        data = TransactionsByCategoryAggregatedGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        period = data.validated_data.get('period')
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_category_transactions_aggregated()

        return Response(response)

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.credit_card
import service.finance.finance
import util.datetime
from core.responses import NotImplementedResponse
from finance.requests.credit_card import CreditCardBillGetSerializer, BillHistorySerializer, CreditCardBillPostSerializer, CreditCardPostSerializer, CreditCardGetSerializer


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get all the active credit cards from user.', parameters=[CreditCardGetSerializer], responses={201: None})
    def get(self, *args, **kwargs):
        data = CreditCardGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user

        response = service.finance.credit_card.CreditCard(owner=user).get_credit_card()

        return Response(response, status=response['statusCode'])

    @extend_schema(description='This endpoint is used to create a new credit card for the user.',
                   summary='This endpoint was not implemented yet.', request=CreditCardPostSerializer, responses={501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        data = CreditCardPostSerializer(data=self.request.data)

        return Response(NotImplementedResponse, status=status.HTTP_501_NOT_IMPLEMENTED)


class CreditCardBill(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the entries from the credit card bill.', parameters=[CreditCardBillGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        validator = CreditCardBillGetSerializer(data=self.request.query_params)
        if not validator.is_valid():
            return Response(validator.errors, status=400)

        credit_card_bill_id = validator.validated_data.get('creditCardBillId')
        period = validator.validated_data.get('period')
        credit_card_id = validator.validated_data.get('creditCardId')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .get_credit_card_bill(period=period, credit_card_id=credit_card_id, credit_card_bill_id=credit_card_bill_id)

        return Response(response, status=response['statusCode'])

    @extend_schema(summary='Create a new entry in credit card bill statement.', request=CreditCardBillPostSerializer, responses={200: None})
    def post(self, *args, **kwargs):
        data = CreditCardBillPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .set_bill(data=data.validated_data, request=self.request)

        return Response(response, status=response['statusCode'])


class BillHistory(APIView):
    @extend_schema(summary='Get the history of the credit card bills.', parameters=[BillHistorySerializer], responses={200: None})
    def get(self, *args, **kwargs):
        data = BillHistorySerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        start_at = data.validated_data.get('startAt')
        end_at = data.validated_data.get('endAt')
        type = data.validated_data.get('type')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user).get_bill_history(history_type=type, start_at=start_at, end_at=end_at)

        return Response(response, status=200)

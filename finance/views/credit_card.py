from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.credit_card
import service.finance.finance
from base.responses import NotImplementedResponse, InvalidRequestError
from finance.requests.credit_card import CreditCardBillGetRequest, BillHistoryRequest, CreditCardBillPostRequest, CreditCardPostRequest, CreditCardGetSerializer
from finance.responses.credit_card import CreditCardBillGetResponse, CreditCardGetResponse


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get all the active credit cards from user.', description='',
                   parameters=[CreditCardGetSerializer], responses={200: CreditCardGetResponse, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = CreditCardGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user

        response = service.finance.credit_card.CreditCard(owner=user).get_credit_card()

        return Response(response, status=response['statusCode'])

    @extend_schema(summary='This endpoint was not implemented yet.', description='This endpoint is used to create a new credit card for the user.',
                   request=CreditCardPostRequest, responses={501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        data = CreditCardPostRequest(data=self.request.data)

        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)


class CreditCardBill(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the entries from the credit card bill.',
                   parameters=[CreditCardBillGetRequest], responses={200: CreditCardBillGetResponse, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        validator = CreditCardBillGetRequest(data=self.request.query_params)
        if not validator.is_valid():
            return Response(validator.errors, status=400)

        credit_card_bill_id = validator.validated_data.get('creditCardBillId')
        period = validator.validated_data.get('period')
        credit_card_id = validator.validated_data.get('creditCardId')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .get_credit_card_bill(period=period, credit_card_id=credit_card_id, credit_card_bill_id=credit_card_bill_id)

        return Response(response, status=response['statusCode'])

    @extend_schema(summary='Create a new entry in credit card bill statement.', request=CreditCardBillPostRequest, responses={201: None})
    def post(self, *args, **kwargs):
        data = CreditCardBillPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .set_bill(data=data.validated_data, request=self.request)

        return Response(response, status=response['statusCode'])


class BillHistory(APIView):
    @extend_schema(summary='Get the history of the credit card bills.', parameters=[BillHistoryRequest], responses={200: None})
    def get(self, *args, **kwargs):
        data = BillHistoryRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        start_at = data.validated_data.get('startAt')
        end_at = data.validated_data.get('endAt')
        type = data.validated_data.get('type')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user).get_bill_history(history_type=type, start_at=start_at, end_at=end_at)

        return Response(response, status=200)

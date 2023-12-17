from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.credit_card
import service.finance.finance
import util.datetime
from finance.serializers.credit_card import CreditCardBillGetSerializer, BillHistorySerializer, CreditCardBillPostSerializer, CreditCardPostSerializer


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user

        response = service.finance.credit_card.CreditCard().get_credit_card()

        return Response(response)

    def post(self, *args, **kwargs):
        serializer = CreditCardPostSerializer(data=self.request.data)


class CreditCardBill(APIView):
    permission_classes = [IsAuthenticated]

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

    def post(self, *args, **kwargs):
        data = CreditCardBillPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .set_bill(data=data.validated_data, request=self.request)

        return Response(response, status=response['statusCode'])


class BillHistory(APIView):
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

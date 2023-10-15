from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.core
import service.finance.finance
from finance.serializers.core import ExpenseGetSerializer
from service.security.security import IsAuthenticated


class Currency(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.core.Core().get_currency()

        return Response(response, status=200)


class Expense(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        data = ExpenseGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        period = data.validated_data.get('period')
        category_id = data.validated_data.get('category_id')

        response = service.finance.core.Core(category_id=category_id, period=period).get_expense()

        return Response(response, status=200)

from rest_framework.response import Response
from rest_framework.views import APIView

import BO.finance.account
from BO.security.security import IsAuthenticated


class Account(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user.id

        response = BO.finance.account.Account(owner=user).get_accounts()

        return Response(response)

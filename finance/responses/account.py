from core.serializers import CustomSerializer
from core.responses import DefaultSuccessResponse
from finance.serializers.account import AccountSerializer


class AccountGetResponse(DefaultSuccessResponse, CustomSerializer):
    accounts = AccountSerializer(many=True)

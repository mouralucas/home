from base.responses import DefaultSuccessResponse
from base.serializers import CustomSerializer
from finance.serializers.account import AccountSerializer, StatementSerializer


class AccountGetResponse(DefaultSuccessResponse, CustomSerializer):
    accounts = AccountSerializer(many=True)


class AccountPostResponse(DefaultSuccessResponse, CustomSerializer):
    account = AccountSerializer()


class StatementGetResponse(DefaultSuccessResponse, CustomSerializer):
    statementEntry = StatementSerializer(many=True)


class StatementPostResponse(DefaultSuccessResponse, CustomSerializer):
    statementEntry = StatementSerializer()

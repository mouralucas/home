from rest_framework import serializers
from base.serializers import CustomSerializer


class StatementPostRequest(CustomSerializer):
    file = serializers.CharField(required=True, help_text='The file to be imported.')
    provider = serializers.CharField(max_length=150, required=True, help_text='The provier of pos (PagSeguro, MercadoPago, etc')
    period = serializers.IntegerField(required=True, help_text='The period of the statement, in yyyymm pattern')



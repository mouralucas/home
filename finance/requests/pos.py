from rest_framework import serializers
from core.serializers import CustomSerializer


class PagSeguroStatementPostRequest(CustomSerializer):
    file = serializers.FileField()
    fileType = serializers.CharField(max_length=5, help_text='The file type (json, csv, xml, etc)')
    period = serializers.IntegerField(help_text='The period of the statement, in yyyymm pattern')


from rest_framework import serializers

from base.serializers import CustomSerializer
import util.datetime


class SummaryGetSerializer(CustomSerializer):
    period = serializers.IntegerField(default=util.datetime.current_period())

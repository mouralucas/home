import uuid

from django.db import models

import core.models


# Create your models here.
class ApiIntegration(core.models.Log):
    service = models.CharField(max_length=100)
    url = models.CharField(max_length=1500)
    headers = models.TextField(null=True)
    body = models.TextField(null=True)
    status_code = models.IntegerField(null=True)
    response = models.TextField(null=True)

    class Meta:
        db_table = 'log"."api_integration'

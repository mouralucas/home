from django.db import models

import core.models


# Create your models here.
class Profile(core.models.Log):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'security"."profile'


class Group(core.models.Log):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'security"."group'


class Access(core.models.Log):
    id = models.CharField(max_length=150, primary_key=True)

    module = models.ForeignKey('core.Module', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'security"."access'

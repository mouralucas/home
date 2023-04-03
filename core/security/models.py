from django.db import models

import core.models


# Create your models here.
class Profile(core.models.Log):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    module = models.ForeignKey('core.Module', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'security"."profile'


class Group(core.models.Log):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'security"."group'


# Former ponto_funcao
class Access(core.models.Log):
    id = models.CharField(max_length=150, primary_key=True)

    module = models.ForeignKey('core.Module', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'security"."access'


class ProfileAccess(core.models.Log):
    profile = models.ForeignKey('security.Profile', on_delete=models.DO_NOTHING)
    access = models.ForeignKey('security.Access', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'security"."profile_access'


class ProfileAccount(core.models.Log):
    profile = models.ForeignKey('security.Profile', on_delete=models.DO_NOTHING)
    account = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    dat_start = models.DateField(null=True)
    dat_end = models.DateField(null=True)

    class Meta:
        db_table = 'security"."profile_account'


class GroupAccount(core.models.Log):
    group = models.ForeignKey('security.Group', on_delete=models.DO_NOTHING)
    account = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=50, null=True)
    dat_start = models.DateField(null=True)
    dat_end = models.DateField(null=True)

    class Meta:
        db_table = 'security"."group_account'

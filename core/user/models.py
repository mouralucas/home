import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

import core.models


class Account(AbstractBaseUser):
    """
    :Name: Account
    :Created by: Lucas Penha de Moura - 09/06/2022
    :Edited by:

    Defines all the accounts available in the system.
    """
    objects = BaseUserManager()

    username = models.CharField(max_length=200, unique=True)
    USERNAME_FIELD = 'username'
    is_staff = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)

    hash = models.UUIDField(null=True, default=uuid.uuid4)
    # level = models.ForeignKey('user.AccountLevel', on_delete=models.DO_NOTHING)
    # type = models.ForeignKey('user.AccountType', on_delete=models.DO_NOTHING)

    # MxN with AccountType

    class Meta:
        db_table = 'public"."account'


# class AccountType(core.models.Log):
#     # PERSONAL_TRAINER = ('personal', _('Personal Trainer'))
#     # STUDENT = ('student', _('Student'))
#     # NUTRITIONIST = ('nutritionist', _('Nutritionist'))
#     # PHYSICAL_THERAPIST = ('physical_therapist', _('Physical Therapist'))
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True)
#
#
# class AccountLevel(core.models.Log):
#     name = models.CharField(max_length=100, null=True)
#     description = models.TextField(null=True)
#
#     class Meta:
#         db_table = 'public"."account_level'

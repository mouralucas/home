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

    class Meta:
        db_table = 'public"."account'

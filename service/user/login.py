import uuid

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import service.core.cache
from service.security.login import CustomAccessToken




from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import service.user.account
import service.security.login

from core.user.serializers import AccountPostSerializer, LoginSerializer, RefreshSerializer, AccountGetSerializer
from service.security.security import IsAuthenticated, CustomJWTAuthentication


class Login(TokenObtainPairView):
    """
    :Name: Login
    :Description: View for user login
    :Created by: Lucas Penha de Moura - 01/02/2021
    :Edited by:

    Explicit params:
    username: the username of the user
    password: the password of the user

        Implements TokenObtainPairView from simple jwt
    """
    serializer_class = LoginSerializer


class Refresh(TokenRefreshView):
    serializer_class = RefreshSerializer


class Account(APIView):
    @extend_schema(
        parameters=[AccountGetSerializer],
        responses={201: None},
    )
    def get(self, *args, **kwargs):
        data = AccountGetSerializer(data=self.request.query_params)
        return render(self.request, '')

    @extend_schema(
        request=AccountPostSerializer,
        responses={201: None}
    )
    def post(self, *args, **kwargs):
        data = AccountPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        username = data.validated_data.get('username')
        raw_password = data.validated_data.get('rawPassword')

        response = service.user.account.Account(username=username, raw_password=raw_password).create()

        return JsonResponse(response, safe=False)


class TestViewWithoutAuth(APIView):

    def get(self, *args, **kwargs):
        return Response({'success': True}, status=status.HTTP_200_OK)


class TestViewWithAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response({'success': True}, status=status.HTTP_200_OK)

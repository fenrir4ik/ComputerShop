from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework import permissions, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from ..APIBase import APIBase


class RegisterAPI(generics.CreateAPIView, APIBase):
    in_arguments = {'username': str, 'email': str, 'password': str}
    out_arguments = {'user': {'id': int, 'username': str, 'email': str}}

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        '''Stringa'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return JsonResponse({"user": UserSerializer(user, context=self.get_serializer_context()).data}, status=status.HTTP_200_OK)


class LoginAPI(KnoxLoginView, APIBase):
    in_arguments = {'username': str, 'password': str}
    out_arguments = {'expiery':str, 'token': str}

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordAPI(generics.UpdateAPIView, APIBase):
    in_arguments = {'old_password': str, 'new_password': str}
    out_arguments = {}

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return JsonResponse({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(KnoxLogoutView, APIBase):
    in_arguments = {}
    out_arguments = {}

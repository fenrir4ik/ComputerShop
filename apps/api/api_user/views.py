from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework import permissions, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from ..APIBase import APIBase


class RegisterAPI(generics.CreateAPIView, APIBase):
    in_arguments = {'username': str, 'email': str, 'password': str}
    out_arguments = {'user': {'id': int, 'username': str, 'email': str}}
    http_methods = ('POST')
    auth_required = False
    call_path = 'api_user/register'

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # token returning while register ?
            # "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView, APIBase):
    in_arguments = {'username': str, 'password': str}
    out_arguments = {'expiery':str, 'token': str}
    http_methods = ('POST')
    auth_required = False
    call_path = 'api_user/login'

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
    http_methods = ('PUT')
    auth_required = True
    call_path = 'api_user/change_password'

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
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(KnoxLogoutView, APIBase):
    in_arguments = {}
    out_arguments = {}
    http_methods = ('POST')
    auth_required = True
    call_path = 'api_user/logout'
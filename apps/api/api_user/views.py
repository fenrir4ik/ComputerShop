from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from ..views import APIBaseView


class RegisterAPI(generics.CreateAPIView, APIBaseView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data}, status=status.HTTP_200_OK)

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'post': {
                'in': {'email': 'string', 'username': 'string', 'password': 'string'},
                'out': {'user': {'id': 'integer','username': 'string','email': 'string'}}
            }
        }
        return super(RegisterAPI, cls).document()


class LoginAPI(KnoxLoginView, APIBaseView):
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'post': {'in': {'username': 'string', 'password': 'string'}, 'out': {'expiry': 'string', 'token': 'string'}}
        }
        return super(LoginAPI, cls).document()


class ChangePasswordAPI(generics.UpdateAPIView, APIBaseView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put']

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"detail": "Wrong old password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'put': {'in': {'old_password': 'string', 'new_password': 'string'}, 'out': {'detail': 'string'}}
        }
        return super(ChangePasswordAPI, cls).document()


class LogoutAPI(KnoxLogoutView, APIBaseView):
    http_method_names = ['post']

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'post': {'in': {}, 'out': {}}
        }
        return super(LogoutAPI, cls).document()

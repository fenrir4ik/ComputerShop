from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserAPITest(APITestCase):
    """
    python manage.py test .\apps\api_user
    """
    def test_user_register(self):
        data = {"username": "TestUser", "email": "testemail@test.com", "password": "test_password"}
        response = self.client.post('/api_user/register/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'TestUser')

    def test_user_login(self):
        User.objects.create_user(username="TestUser", password='test_password', email="testemail@test.com")
        data = {"username": "TestUser", "password": "test_password"}
        response = self.client.post('/api_user/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_logout(self):
        User.objects.create_user(username="TestUser", password='test_password', email="testemail@test.com")

        login_data = {"username": "TestUser", "password": "test_password"}
        response = self.client.post('/api_user/login/', login_data)
        token = response.data['token']

        header = {'HTTP_AUTHORIZATION': f"Token {token}"}
        response = self.client.post('/api_user/logout/', **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_change_password(self):
        User.objects.create_user(username="TestUser", password='test_password', email="testemail@test.com")

        login_data = {"username": "TestUser", "password": "test_password"}
        response = self.client.post('/api_user/login/', login_data)
        token = response.data['token']

        header = {'HTTP_AUTHORIZATION': f"Token {token}"}
        data = {"old_password": "test_password", "new_password": "new_test_password"}
        response = self.client.put('/api_user/change_password/', data = data, **header)

        changed_user = User.objects.get(username="TestUser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(changed_user.check_password("new_test_password"))

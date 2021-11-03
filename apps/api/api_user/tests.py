from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class ApiUserTest(APITestCase):
    """
    python manage.py test .\apps\api\api_user

    API urls:
    api_user/login/
    api_user/logout/
    api_user/register/
    api_user/change_password/

    """

    def setUp(self):
        user_data = dict(username="TestUser", password='test_password', email="testemail@test.com")
        User.objects.create_user(**user_data)
        self.login_data = {"username": user_data['username'], "password": user_data['password']}
        self.relative_path = '/api/api_user/'

    def test_user_register(self):
        data = {"username": "TestUserRegister", "email": "testemailregister@test.com", "password": "test_password"}
        response = self.client.post(self.relative_path + 'register/', data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['user']['username'], 'TestUserRegister')

    def test_user_login(self):
        response = self.client.post(self.relative_path + 'login/', self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_logout(self):
        response = self.client.post(self.relative_path + 'login/', self.login_data)
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': f"Token {token}"}

        response = self.client.post(self.relative_path + 'logout/', **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(self.relative_path + 'logout/', **header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_change_password(self):
        response = self.client.post(self.relative_path + 'login/', self.login_data)
        token = response.data['token']

        header = {'HTTP_AUTHORIZATION': f"Token {token}"}
        data = {"old_password": "test_password", "new_password": "new_test_password"}
        response = self.client.put(self.relative_path + 'change_password/', data, **header)

        changed_user = User.objects.get(username="TestUser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(changed_user.check_password("new_test_password"))

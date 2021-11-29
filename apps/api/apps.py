import sys
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'


    # print(requests.get('http://127.0.0.1:8000/api/api_user/login/'))
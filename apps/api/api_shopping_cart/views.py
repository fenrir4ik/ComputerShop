from django.db import connection
from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response


class TestApi(generics.ListAPIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        print('Get')

        try:
            with connection.cursor() as cursor:
                mas = [10, 4, 3]
                cursor.execute("call add_product_to_cart({}, {}, {})".format(*mas))
        except Exception as ex:
            print(ex)
            print('except')
            pass
        return Response({})
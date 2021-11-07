from django.db import connection, transaction, DatabaseError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Characteristics, ProductType, ProductCharacteristics
from .serializers import ProductSerializer, ProductCharacteristicsSerializer, TypeSerializer, \
    TypeCharacteristicsSerializer, ProductCharacteristicsDisplaySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['product_price']
    ordering = ['product_price']

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.all().order_by('id')


class ProductCharacteristicsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCharacteristicsSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Characteristics.objects.all()
    http_method_names = ['get', 'put', 'delete']

    def get_object(self):
        id = self.request.parser_context.get('kwargs').get('pk')
        return get_object_or_404(Product, pk=id)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product_characteristics = self.get_product_characteristics(product)
        serializer = ProductCharacteristicsDisplaySerializer(product_characteristics, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        chars_list = self.retrieve_chars_list(request)
        self.set_product_chars(product, chars_list)
        product_characteristics = self.get_product_characteristics(product)
        serializer = ProductCharacteristicsDisplaySerializer(product_characteristics, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        self.delete_chars(product)
        return Response(status=status.HTTP_200_OK)

    def get_product_characteristics(self, product):
        return ProductCharacteristics.objects.filter(product_id=product.id).all()

    def delete_chars(self, product_instance):
        for char in product_instance.product_characteristics.all():
            product_instance.product_characteristics.remove(char)
            if not ProductCharacteristics.objects.select_related('char_name') \
                .filter(char_name__char_name=char.char_name) \
                .exists():
                char.delete()
        product_instance.save()
        print(product_instance.product_characteristics.all())

    def retrieve_chars_list(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        chars_list = serializer.data if is_many else [serializer.data]
        return chars_list

    def set_product_chars(self, product_instance, chars_list):
        self.delete_chars(product_instance)
        for char in chars_list:
            try:
                with transaction.atomic():
                    obj, created = Characteristics.objects.get_or_create(char_name=char.get('char_name'))
                    product_instance.product_characteristics.add(obj, through_defaults={
                        'char_value': char.get('char_value')})
            except DatabaseError:
                print('true')
                product_instance.product_characteristics.clear()
            finally:
                product_instance.save()


class ProductTypeCharacteristicsAPI(generics.ListAPIView):
    serializer_class = TypeCharacteristicsSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    def get_object(self):
        id = self.request.parser_context.get('kwargs').get('pk')
        return get_object_or_404(ProductType, pk=id)

    def get(self, request, *args, **kwargs):
        product_type = self.get_object()
        product_type_chars = self.get_product_type_characteristics(product_type.id)

        result_dict = {}
        for char_name, char_value in product_type_chars:
            if char_name in result_dict:
                result_dict[char_name].append(char_value)
            else:
                result_dict[char_name] = [char_value]
        data = {'characteristcs_list': result_dict}

        serializer = self.get_serializer(data=data)
        serializer.is_valid()

        return Response({**serializer.data}, status=status.HTTP_200_OK)

    def get_product_type_characteristics(self, pt_id):
        sql_query = """SELECT DISTINCT t1.char_name, t2.char_value 
                       FROM characteristics t1
                       JOIN product_chars t2 on t1.id = t2.char_id
                       JOIN product t3 on t3.id = t2.product_id
                       JOIN product_type t4 on t4.id = t3.product_type_id
                       WHERE t4.id = %s
                       """
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [pt_id])
            return cursor.fetchall()


class ProductTypeAPI(generics.ListAPIView):
    serializer_class = TypeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = ProductType.objects.all()
    pagination_class = None
    http_method_names = ['get']


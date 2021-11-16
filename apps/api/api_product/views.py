from django.db import transaction, DatabaseError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Characteristics, ProductType, ProductCharacteristics
from .serializers import ProductSerializerDisplay, ProductCharacteristicsSerializer, TypeSerializer, \
    ProductCharacteristicsDisplaySerializer, ProductSerializer
from .utils import API_SHOPPING_CART_in_any_cart


class ProductViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['product_price']
    ordering = ['product_price']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return ProductSerializerDisplay
        else:
            return ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not API_SHOPPING_CART_in_any_cart(instance.id):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"detail": ["Product exists in shopping cart of user"]}, status=status.HTTP_403_FORBIDDEN)


class ProductCharacteristicsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCharacteristicsSerializer
    queryset = Characteristics.objects.all()
    http_method_names = ['get', 'put', 'delete', 'options']

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

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
        if len(chars_list) == 0:
            return Response({"detail": ["Characteristics list is empty"]}, status=status.HTTP_400_BAD_REQUEST)
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
            if not ProductCharacteristics.objects.select_related('char') \
                .filter(char__char_name=char.char_name) \
                .exists():
                char.delete()
        product_instance.save()

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
                product_instance.product_characteristics.clear()
            finally:
                product_instance.save()


class ProductTypeAPI(generics.ListAPIView):
    serializer_class = TypeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = ProductType.objects.all()
    pagination_class = None
    http_method_names = ['get', 'options']


from django.db import transaction, DatabaseError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Characteristics, ProductType, ProductCharacteristics, Vendor
from .serializers import ProductSerializerDisplay, ProductCharacteristicsSerializer, TypeSerializer, \
    ProductCharacteristicsDisplaySerializer, ProductSerializer, VendorSerializer
from ..views import APIBaseView


class ProductViewSet(viewsets.ModelViewSet, APIBaseView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['product_price']
    ordering = ['id']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return ProductSerializerDisplay
        else:
            return ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({"detail": ["Product exists in shopping cart of user"]}, status=status.HTTP_403_FORBIDDEN)

    @classmethod
    def document(cls, **kwargs) -> dict:
        if not kwargs.get("details", False):
            cls.doc = {
                'get': {
                    'in': {'product_price_min': 'number', 'product_price_max': 'number', 'product_type': 'integer',
                           'product_vendor': 'integer', 'search': 'string', 'ordering': 'string'},
                    'out': {'count': 'integer', 'next': 'string', 'previous': 'string',
                            'results': {'id': 'integer', 'product_type': 'string', 'product_vendor': 'string',
                                        'product_characteristics': {'char_name': 'string', 'char_value': 'string'},
                                        'product_name': 'string', 'product_price': 'number',
                                        'product_amount': 'integer', 'product_description': 'string',
                                        'product_image': 'image'}}
                },
                'post': {
                    'in': {'product_name': 'string', 'product_price': 'number', 'product_amount': 'integer',
                           'product_description': 'string', 'product_image': 'image', 'product_type': 'integer',
                           'product_vendor': "integer"},
                    'out': {'id': 'integer', 'product_name': 'string', 'product_price': 'number',
                            'product_amount': 'integer',
                            'product_description': 'string', 'product_image': 'image', 'product_type': 'integer',
                            'product_vendor': "integer"}
                }
            }
        else:
            product = {'id': 'integer', 'product_type': 'string', 'product_vendor': 'string',
                       'product_name': 'string', 'product_price': 'number',
                       'product_amount': 'integer', 'product_description': 'string',
                       'product_image': 'image'}
            cls.doc = {
                'get': {'in': {'id': 'integer'}, 'out': product},
                'put': {'in': product, 'out': product},
                'patch': {'in': product, 'out': product},
                'delete': {'in': {'id': 'integer'}, 'out': {'detail': 'string'}}
            }
        return super(ProductViewSet, cls).document()


class ProductCharacteristicsAPI(generics.RetrieveUpdateDestroyAPIView, APIBaseView):
    serializer_class = ProductCharacteristicsSerializer
    queryset = Characteristics.objects.all()
    http_method_names = ['get', 'put', 'delete']

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_object(self):
        product_id = self.request.parser_context.get('kwargs').get('pk')
        return get_object_or_404(Product, pk=product_id)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product_characteristics = self.get_product_characteristics(product)
        serializer = ProductCharacteristicsDisplaySerializer(product_characteristics, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

    def retrieve_chars_list(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        chars_list = serializer.data if is_many else [serializer.data]
        return chars_list

    def delete_chars(self, product_instance):
        try:
            with transaction.atomic():
                for char in product_instance.product_characteristics.select_for_update():
                    product_instance.product_characteristics.remove(char)
                    Characteristics.objects.filter(char_name=char.char_name, products=None).delete()
        except DatabaseError:
            pass

    def set_product_chars(self, product_instance, chars_list):
        try:
            with transaction.atomic():
                self.delete_chars(product_instance)
                for char in chars_list:
                    obj, created = Characteristics.objects.get_or_create(char_name=char.get('char_name'))
                    product_instance.product_characteristics.add(obj, through_defaults={
                        'char_value': char.get('char_value')})
        except DatabaseError:
            pass

    @classmethod
    def document(cls, **kwargs) -> dict:
        if kwargs.get("details", True):
            cls.doc = {
                'get': {'in': {'id': 'integer'}, 'out': {'list': {'char_value': 'string', 'char_name': 'string'}}},
                'put': {'in': {'id': 'integer', 'list': {'char_value': 'string', 'char_name': 'string'}}, 'out': {}},
                'delete': {'in': {'id': 'integer'}, 'out': {}},
            }
        return super(ProductCharacteristicsAPI, cls).document()


class ProductTypeAPI(generics.ListAPIView, APIBaseView):
    serializer_class = TypeSerializer
    permission_classes = (AllowAny,)
    queryset = ProductType.objects.all()
    pagination_class = None
    http_method_names = ['get']

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'get': {'in': {}, 'out': {'list': {'id': 'integer', 'type_name': 'string'}} }
        }
        return super(ProductTypeAPI, cls).document()


class ProductVendorAPI(generics.ListAPIView, APIBaseView):
    serializer_class = VendorSerializer
    permission_classes = (AllowAny,)
    queryset = Vendor.objects.all()
    pagination_class = None
    http_method_names = ['get']

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'get': {'in': {}, 'out': {'list': {'id': 'integer', 'vendor_name': 'string'}}}
        }
        return super(ProductVendorAPI, cls).document()

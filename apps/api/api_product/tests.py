import io

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.api_product.models import ProductType, Product, Vendor, Country, Characteristics, ProductCharacteristics


class ApiUserTest(APITestCase):
    """
    python manage.py test .\apps\api\api_product

    API urls:
    api_product/product/
    api_product/product/{id}/
    api_product/product_characteristics/{id}/
    api_product/product_types/

    #       ++product/
    #       ++product/?page=2
    #       ++product/?page=2&type=5&asc desc&!!!!
    #       ++product/2 GET
    #       ++product/ POST
    #       ++product/2 DELETE
    #       ++product/2 UPDATE
    #       ++characteristics POST/DELETE/UPDATE TO PRODUCT
    #       ++get all types


    """

    def setUp(self):
        user = User.objects.create(username='test', is_staff=True)
        user.set_password('12121212')
        user.save()

        self.client.login(username='test', password='12121212')
        self.unauthorized_client = Client()

        product_type_list = [
            ProductType(id=1, type_name="Видеокарты"),
            ProductType(id=2, type_name="Процессоры"),
            ProductType(id=3, type_name="Блоки питания")
        ]
        ProductType.objects.bulk_create(product_type_list)

        country_list = [
            Country(id=1, country_name="Китай"),
            Country(id=2, country_name="США"),
        ]
        Country.objects.bulk_create(country_list)

        vendor_list = [
            Vendor(id=1, vendor_country = country_list[0], vendor_email="vendor1.test@gmail.com",
                   vendor_description="Производитель из Китая", vendor_name="AsRock"),
            Vendor(id=2, vendor_country=country_list[1], vendor_email="vendor2.test@gmail.com",
                   vendor_description="Производитель из США", vendor_name="NVidia")
        ]
        Vendor.objects.bulk_create(vendor_list)

        product_list = [
            Product(id=2,product_type=product_type_list[0], product_vendor=vendor_list[0], product_name='GTX 1660 TI',
                    product_price=22000, product_amount=3, product_description="Видеокарта прямо из Китая",
                    product_image='TEST0.png'),
            Product(id=3,product_type=product_type_list[0], product_vendor=vendor_list[1], product_name='RTX 2070',
                    product_price=26000, product_amount=3, product_description="Видеокарта прямо из США",
                    product_image='TEST1.png'),
            Product(id=4,product_type=product_type_list[0], product_vendor=vendor_list[1], product_name='RTX 2060',
                    product_price=26000, product_amount=3, product_description="Видеокарта прямо из США",
                    product_image='TEST2.png')
        ]
        Product.objects.bulk_create(product_list)

        chars_names_list = [
            Characteristics(char_name="Частота памяти"),
            Characteristics(char_name="Объем памяти"),
            Characteristics(char_name="Частота ядра"),
            Characteristics(char_name="Тип памяти"),
        ]
        Characteristics.objects.bulk_create(chars_names_list)

        product_chars_list = [
            ProductCharacteristics(product=product_list[0], char=chars_names_list[0], char_value="12000 МГц"),
            ProductCharacteristics(product=product_list[0], char=chars_names_list[1], char_value="6 ГБ"),
            ProductCharacteristics(product=product_list[0], char=chars_names_list[2], char_value="1800 МГц"),
            ProductCharacteristics(product=product_list[1], char=chars_names_list[1], char_value="6 ГБ"),
            ProductCharacteristics(product=product_list[1], char=chars_names_list[2], char_value="1680 МГц"),
            ProductCharacteristics(product=product_list[1], char=chars_names_list[3], char_value="GDDR6"),
            ProductCharacteristics(product=product_list[2], char=chars_names_list[0], char_value="12200 МГц"),
            ProductCharacteristics(product=product_list[2], char=chars_names_list[2], char_value="1680 МГц"),
            ProductCharacteristics(product=product_list[2], char=chars_names_list[3], char_value="GDDR6"),
        ]
        ProductCharacteristics.objects.bulk_create(product_chars_list)

    def test_product_list(self):
        response = self.client.get(reverse('Products List'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3)
        self.assertEqual(response.data.get('next'), None)
        self.assertEqual(response.data.get('previous'), None)
        self.assertEqual(len(response.data.get('results')), 3)


    def test_product_filtering(self):
        response = self.client.get(reverse('Products List'), {'product_type': 1})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Products List'), {'product_type': 2})
        self.assertEqual(len(response.data.get('results')), 0)
        response = self.client.get(reverse('Products List'), {'product_vendor': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('Products List'), {'product_type': 1, 'product_vendor': 1})
        self.assertEqual(len(response.data.get('results')), 1)
        response = self.client.get(reverse('Products List'), {'product_type': 1, 'product_vendor': 2})
        self.assertEqual(len(response.data.get('results')), 2)
        response = self.client.get(reverse('Products List'), {'product_type': 1, 'product_vendor': (1, 2)})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Products List'), {'product_type': 1, 'product_vendor': (1, 2, 3)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('Products List'), {'product_price_min': 16000, 'product_price_max': 24000})
        self.assertEqual(len(response.data.get('results')), 1)
        response = self.client.get(reverse('Products List'), {'product_price_min': 16000, 'product_price_max': 27000})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Products List'), {'product_price_min': 16000})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Products List'), {'product_price_max': 16000})
        self.assertEqual(len(response.data.get('results')), 0)


    def test_product_add(self):
        vendor = Vendor.objects.get(pk=1)
        product_type=ProductType.objects.get(pk=1)
        with open("media/product/TEST.png", 'rb') as image:
            image_file = io.FileIO(image.fileno())
            product_data = dict(product_type=product_type.id, product_vendor=vendor.id, product_name='RTX 2060',
                        product_price=26000, product_amount=3, product_description="Видеокарта прямо из США",
                        product_image=image)

            print(product_data)
            # response = self.unauthorized_client.post(reverse('Products List'), product_data)
            # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            response = self.client.post(reverse('Products List'), product_data, format='multipart')
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_product_update(self):
    #     pass
    #
    # def test_product_partial_update(self):
    #     pass
    #
    # def test_product_delete(self):
    #     pass
    #
    # def test_product_details(self):
    #     pass
    #
    # def test_product_types_retrieve(self):
    #     response = self.client.get(self.relative_path + 'product_types/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 3)
    #     self.assertEqual(response.data[0].get('type_name'), "Видеокарты")
    #
    # def test_product_characteristics_add(self):
    #     pass
    #
    # def test_product_characteristics_delete(self):
    #     pass
    #
    # def test_product_characteristics_update(self):
    #     pass

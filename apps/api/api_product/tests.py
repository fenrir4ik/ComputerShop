import os
import uuid

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.api_product.models import ProductType, Product, Vendor, Country, Characteristics, ProductCharacteristics


class ImageData:
    image = None
    image_name = None
    test_folder_name = None
    products_folder_name = settings.MEDIA_ROOT + '\product\\'

    def create_image_data(self):
        self.test_folder_name = self.products_folder_name + 'test' + str(uuid.uuid4()) + '\\'
        self.image_name = str(uuid.uuid4()) + '.png'
        self.generate_image_file(self.test_folder_name, self.image_name)
        self.image = open(self.test_folder_name + self.image_name, 'rb')

    def generate_image_file(self, folder, name):
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        image = Image.new('RGB', (512, 512))
        image.save(folder+name)

    def delete_image_data(self):
        self.image.close()
        remove_list = [self.products_folder_name + self.image_name, self.test_folder_name + self.image_name]
        for file in remove_list:
            try:
                os.remove(file)
            except FileNotFoundError:
                continue
        try:
            os.rmdir(self.test_folder_name)
        except FileNotFoundError:
            pass


class ApiUserTest(APITestCase, ImageData):
    """
    python manage.py test .\apps\api\api_product

    API urls:
    api_product/product/
    api_product/product/{id}/
    api_product/product_characteristics/{id}/
    api_product/product_types/
    """
    def setUp(self):
        user = User.objects.create(username='test', is_staff=True)
        user.set_password('12121212')
        user.save()
        self.client.login(username='test', password='12121212')

        self.create_image_data()

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

    def tearDown(self):
        self.delete_image_data()

    def test_product_list(self):
        response = self.client.get(reverse('Product API:Product List'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3)
        self.assertEqual(response.data.get('next'), None)
        self.assertEqual(response.data.get('previous'), None)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_product_filtering(self):
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 1})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 2})
        self.assertEqual(len(response.data.get('results')), 0)
        response = self.client.get(reverse('Product API:Product List'), {'product_vendor': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 1, 'product_vendor': 1})
        self.assertEqual(len(response.data.get('results')), 1)
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 1, 'product_vendor': 2})
        self.assertEqual(len(response.data.get('results')), 2)
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 1, 'product_vendor': (1, 2)})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Product API:Product List'), {'product_type': 1, 'product_vendor': (1, 2, 3)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('Product API:Product List'), {'product_price_min': 16000, 'product_price_max': 24000})
        self.assertEqual(len(response.data.get('results')), 1)
        response = self.client.get(reverse('Product API:Product List'), {'product_price_min': 16000, 'product_price_max': 27000})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Product API:Product List'), {'product_price_min': 16000})
        self.assertEqual(len(response.data.get('results')), 3)
        response = self.client.get(reverse('Product API:Product List'), {'product_price_max': 16000})
        self.assertEqual(len(response.data.get('results')), 0)

    def test_product_add(self):
        vendor = Vendor.objects.get(pk=1)
        product_type=ProductType.objects.get(pk=1)
        product_data = dict(product_type=product_type.id, product_vendor=vendor.id, product_name='TEST',
                    product_price=26000, product_amount=3, product_description="Видеокарта прямо из США",
                    product_image=self.image)
        response = self.client.post(reverse('Product API:Product List'), product_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(pk=1).product_name, 'TEST')
        self.client.logout()
        response = self.client.post(reverse('Product API:Product List'), product_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_details(self):
        response = self.client.get(reverse('Product API:Product Details', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), 2)
        self.assertEqual(len(response.data.get('product_characteristics')), 3)
        response = self.client.get(reverse('Product API:Product Details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_update(self):
        partial_data = {"product_type": 1, "product_name": "GTX 1660 TI NEW"}
        product = Product.objects.get(pk=2)
        put_data = dict(product_name='GTX 1660 TI NEW', product_price=28000, product_amount=product.product_amount,
                        product_description=product.product_description, product_image=self.image,
                        product_type=product.product_type_id, product_vendor=product.product_vendor.id)
        response = self.client.put(reverse('Product API:Product Details', kwargs={'pk': 2}), partial_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(reverse('Product API:Product Details', kwargs={'pk': 2}), put_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("product_name"), "GTX 1660 TI NEW")
        self.client.logout()
        response = self.client.put(reverse('Product API:Product Details', kwargs={'pk': 2}), put_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('Product API:Product Details', kwargs={'pk': 2}), partial_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_product_partial_update(self):
        data = {"product_type": 1, "product_name": "GTX 1660 TI NEW"}
        response = self.client.patch(reverse('Product API:Product Details', kwargs={'pk': 2}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('product_name'), "GTX 1660 TI NEW")
        self.client.logout()
        response = self.client.patch(reverse('Product API:Product Details', kwargs={'pk': 2}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_delete(self):
        response = self.client.delete(reverse('Product API:Product Details', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('Product API:Product Details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        response = self.client.delete(reverse('Product API:Product Details', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_types_retrieve(self):
        response = self.client.get(reverse('Product API:Product Types'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get('type_name'), "Видеокарты")

    def test_product_characteristics_get(self):
        response = self.client.get(reverse('Product API:Product Characteristics', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        response = self.client.get(reverse('Product API:Product Characteristics', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_product_characteristics_add(self):
        chars = [ {"char_name": "Тип памяти", "char_value": "DDR4"},
                            {"char_name": "Частота памяти", "char_value": "2400"} ]
        chars_larger = chars + [{"char_name": "Объем памяти", "char_value": "8 ГБ"}]
        response = self.client.put(reverse('Product API:Product Characteristics', kwargs={'pk': 2}), chars, format='json')
        product_characteristics_result = Product.objects.get(pk=2).product_characteristics
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product_characteristics_result.count(), 2)
        self.assertEqual(product_characteristics_result.filter(char_name="Тип памяти").count(), 1)
        response = self.client.put(reverse('Product API:Product Characteristics', kwargs={'pk': 2}), chars_larger, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product_characteristics_result.count(), 3)
        self.assertEqual(product_characteristics_result.filter(char_name="Тип памяти").count(), 1)
        response = self.client.put(reverse('Product API:Product Characteristics', kwargs={'pk': 3}), chars_larger, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product_characteristics_result.count(), 3)
        response = self.client.put(reverse('Product API:Product Characteristics', kwargs={'pk': 3}), [], format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('detail' in response.data)
        self.client.logout()
        response = self.client.put(reverse('Product API:Product Characteristics', kwargs={'pk': 2}), chars, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_characteristics_delete(self):
        product_characteristics = Product.objects.get(pk=2).product_characteristics
        untouched_product = Product.objects.get(pk=3).product_characteristics
        characteristics = Characteristics.objects
        response = self.client.delete(reverse('Product API:Product Characteristics', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_characteristics.count(), 0)
        self.assertEqual(untouched_product.count(), 3)
        self.assertEqual(characteristics.count(), 4)
        response = self.client.delete(reverse('Product API:Product Characteristics', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_characteristics.count(), 0)
        self.assertEqual(untouched_product.count(), 0)
        self.assertEqual(characteristics.count(), 3)
        self.client.logout()
        response = self.client.delete(reverse('Product API:Product Characteristics', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

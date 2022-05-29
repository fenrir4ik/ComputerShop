from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from apps.core.models import User
from apps.store.forms import CreateOrderForm
from apps.store.models import PaymentType
from apps.store.views import OrderCreateView


class OrderCreateFormValidationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/orders/create/')
        self.form_class = CreateOrderForm

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test.test@gmail.com',
                                            name='Test',
                                            surname='Testov',
                                            patronymic='Testovich',
                                            phone_number='380506785423',
                                            password='test12121212')
        cls.superuser = User.objects.create_superuser(email='test.supertest@gmail.com',
                                                      name='Test',
                                                      surname='Testov',
                                                      patronymic='Testovich',
                                                      phone_number='380506785423',
                                                      password='test12121212')
        PaymentType(id=1, type='Оплата картой').save()

    def test_valid_input(self):
        valid_data = {'name': 'Test', 'surname': 'Testov', 'patronymic': 'Testovich', 'phone_number': '380505653456',
                      'email': 'test.test@gmail.com', 'address': 'Nauki 7', 'payment': 1}
        self.form = self.form_class(user=self.user, data=valid_data)

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.errors == {})

    def test_invalid_input(self):
        invalid_data = {'name': 'Test3', 'surname': 'Testov3', 'patronymic': 'Testovich3',
                        'phone_number': '546324543653', 'email': '4444email', 'address': 'Nauki 7', 'payment': 5}
        self.form = self.form_class(user=self.user, data=invalid_data)

        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['name'][0],
                         'Имя должно состоять только из букв латиницы или кириллицы.')
        self.assertEqual(self.form.errors['surname'][0],
                         'Фамилия должна состоять только из букв латиницы или кириллицы.')
        self.assertEqual(self.form.errors['patronymic'][0],
                         'Отчество должно состоять только из букв латиницы или кириллицы.')
        self.assertEqual(self.form.errors['phone_number'][0],
                         'Номер телефона должен быть длинной в 12 символов и начинаться с 380.')
        self.assertEqual(self.form.errors['email'][0],
                         'Введите правильный адрес электронной почты.')
        self.assertEqual(self.form.errors['payment'][0],
                         'Выберите корректный вариант. Вашего варианта нет среди допустимых значений.')


class OrderCreatePageSecurityTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/orders/create/')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test.test@gmail.com',
                                            name='Test',
                                            surname='Testov',
                                            patronymic='Testovich',
                                            phone_number='380506785423',
                                            password='test12121212')
        cls.superuser = User.objects.create_superuser(email='test.supertest@gmail.com',
                                                      name='Test',
                                                      surname='Testov',
                                                      patronymic='Testovich',
                                                      phone_number='380506785423',
                                                      password='test12121212')

    def test_order_by_anonymous_user(self):
        self.request.user = AnonymousUser()
        response = OrderCreateView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def test_order_by_manager(self):
        self.request.user = self.superuser
        response = OrderCreateView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def test_order_by_client(self):
        self.request.user = self.user
        response = OrderCreateView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

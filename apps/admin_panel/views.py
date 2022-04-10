from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, UpdateView

from apps.admin_panel.filters import AdminProductFilter, AdminOrderFilter
from apps.admin_panel.forms import ProductAddForm, ProductUpdateForm, OrderChangeForm
from apps.core.permissions import ManagerPermissionMixin
from apps.store.models import Product
from db.characteristic_dao import CharacteristicDAO
from db.order_dao import OrderDAO
from db.product_dao import ProductDAO
from services.constants import DEFAULT_PRODUCT_IMAGE, PRODUCT_IMAGE_MAX_AMOUNT


class ProductsListAdminView(ManagerPermissionMixin, ListView):
    """View is used for displaying products list and products add form in admin-panel"""
    template_name = 'admin_panel/products_list.html'
    context_object_name = 'products'
    paginate_by = 10
    form_class = ProductAddForm
    success_url = reverse_lazy('admin-products')

    def get_queryset(self):
        # amount and date_created not used
        queryset = ProductDAO.get_products_list()
        queryset = queryset.values('id', 'image', 'name', 'price', 'amount', 'vendor__name', 'category__name',
                                   'date_created')
        queryset = queryset.order_by('-id')
        filter = AdminProductFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_form(self):
        if self.request.method == 'POST':
            return self.form if hasattr(self, 'form') else self.form_class(self.request.POST, self.request.FILES)
        else:
            return self.form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdminProductFilter(self.request.GET)
        context['form'] = self.get_form()
        context['max_img_num'] = PRODUCT_IMAGE_MAX_AMOUNT
        return context

    def post(self, request, *args, **kwargs):
        self.form = self.get_form()
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.get(request, *args, **kwargs)


class ProductDeleteView(ManagerPermissionMixin, DeleteView):
    """View is used for deletion products in admin-panel"""
    error_message = "Товар №{} находится в корзине пользователя и не может быть удален"
    success_message = "Товар №{} был успешно удален"
    model = Product

    def form_valid(self, form):
        success_url = self.get_success_url()
        deleted = ProductDAO.delete_product(self.object.pk)
        if deleted:
            message_tuple = (self.request, messages.SUCCESS, self.success_message.format(self.object.pk))
        else:
            message_tuple = (self.request, messages.ERROR, self.error_message.format(self.object.pk))
        if len(get_messages(self.request)) == 0:
            messages.add_message(*message_tuple)
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        return next_page if next_page else reverse_lazy('admin-products')


class ProductUpdateView(ManagerPermissionMixin, UpdateView):
    """View is used for updating products in admin-panel"""
    template_name = 'admin_panel/update_product.html'
    form_class = ProductUpdateForm
    context_object_name = 'product'

    def get_queryset(self):
        return ProductDAO.get_products_list(include_price=True, include_image=False)

    def get_success_url(self):
        return reverse('product-update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_product_image'] = DEFAULT_PRODUCT_IMAGE
        context['product_characteristics'] = CharacteristicDAO.get_product_characteristics(self.object.pk)
        return context


class OrdersListView(ManagerPermissionMixin, ListView):
    """View is used for displaying orders list in admin-panel"""
    template_name = 'store/user_orders.html'
    context_object_name = 'orders_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdminOrderFilter(self.request.GET)
        return context

    def get_queryset(self):
        queryset = OrderDAO.get_all_orders()
        queryset = queryset.order_by('-id')
        filter = AdminOrderFilter(self.request.GET, queryset=queryset)
        return filter.qs


class OrderUpdateView(ManagerPermissionMixin, UpdateView):
    """View is used for updating orders in admin-panel"""
    template_name = 'admin_panel/update_order.html'
    form_class = OrderChangeForm
    context_object_name = 'order'

    def get_queryset(self):
        return OrderDAO.get_all_orders()

    def get_success_url(self):
        return self.request.path_info

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

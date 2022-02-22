from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from apps.admin_panel.filters import AdminProductFilter
from apps.admin_panel.forms import ProductAddForm, ProductUpdateForm, OrderChangeForm
from apps.core.permissions import WarehousePermissionMixin, ManagerPermissionMixin
from apps.store.models import Product
from db.order_dao import OrderDAO
from db.product_dao import ProductDAO
from services.constants import DEFAULT_PRODUCT_IMAGE


class ProductAddView(WarehousePermissionMixin, CreateView):
    """View is used for products creation via admin panel"""
    template_name = 'admin_panel/add_product.html'
    form_class = ProductAddForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('product-update', kwargs={'pk': self.object.pk})


class ProductsListAdminView(WarehousePermissionMixin, ListView):
    """View is used for displaying products list in admin-panel"""
    template_name = 'admin_panel/products_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['filter'] = AdminProductFilter(self.request.GET)
        return context

    def get_queryset(self):
        # amount and date_created not used
        queryset = ProductDAO.get_products_list()
        queryset = queryset.values('id', 'image', 'name', 'price', 'amount', 'vendor__name', 'category__name',
                                   'date_created')
        queryset = queryset.order_by('-id')
        filter = AdminProductFilter(self.request.GET, queryset=queryset)
        return filter.qs



class ProductDeleteView(WarehousePermissionMixin, DeleteView):
    """View is used for deletion products in admin-panel"""
    template_name = 'admin_panel/delete_product.html'
    success_url = reverse_lazy('admin-products')
    context_object_name = 'product'
    error_message = "Товар №{} находится в корзинах пользователя и не может быть удален"
    success_message = "Товар №{} был успешно удален"

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Product, id=id_)

    def form_valid(self, form):
        success_url = self.get_success_url()
        deleted = ProductDAO.delete_product(self.object.pk)
        if deleted:
            messages.success(self.request, self.success_message.format(self.object.pk))
        else:
            messages.error(self.request, self.error_message.format(self.object.pk))
        return HttpResponseRedirect(success_url)


class ProductUpdateView(WarehousePermissionMixin, UpdateView):
    """View is used for updating products in admin-panel"""
    template_name = 'admin_panel/update_product.html'
    form_class = ProductUpdateForm

    def get_queryset(self):
        return ProductDAO.get_products_list(include_price=True, include_image=False)

    def get_success_url(self):
        return reverse('product-update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['default_product_image'] = DEFAULT_PRODUCT_IMAGE
        return context


class OrdersListView(ManagerPermissionMixin, ListView):
    """View is used for displaying orders list in admin-panel"""
    template_name = 'store/user_orders.html'
    context_object_name = 'orders_list'

    def get_queryset(self):
        return OrderDAO.get_all_orders().order_by('id')


class OrderUpdateView(ManagerPermissionMixin, UpdateView):
    """View is used for updating orders in admin-panel"""
    template_name = 'admin_panel/update_order.html'
    form_class = OrderChangeForm
    context_object_name = 'order'

    def get_queryset(self):
        return OrderDAO.get_all_orders()

    def get_success_url(self):
        return self.request.path_info

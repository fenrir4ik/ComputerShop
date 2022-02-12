from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from apps.admin_panel.forms import ProductAddForm, ProductUpdateForm
from apps.store.models import Product
from computershop.settings import DEFAULT_PRODUCT_IMAGE
from services.dao.product_dao import ProductDAO


class ProductAddView(CreateView):
    """
    View is used for products creation via admin panel
    """
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
        return reverse('update product', kwargs={'pk': self.object.pk})


class ProductsListAdminView(ListView):
    """
    View is used for displaying products list in admin-panel
    """
    template_name = 'admin_panel/products_list.html'
    context_object_name = 'products'
    paginate_by = 20

    # Filters needed
    # paginate_by = 20

    def get_queryset(self):
        queryset = ProductDAO.get_products_list()
        return queryset.values('id', 'image', 'name', 'price', 'amount', 'vendor__name', 'category__name',
                               'date_created').order_by('pk')


class ProductDeleteView(DeleteView):
    template_name = 'admin_panel/delete_product.html'
    success_url = reverse_lazy('admin products')
    context_object_name = 'product'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Product, id=id_)

    def form_valid(self, form):
        success_url = self.get_success_url()
        ProductDAO.delete_product(self.object)
        return HttpResponseRedirect(success_url)


class ProductUpdateView(UpdateView):
    template_name = 'admin_panel/update_product.html'
    form_class = ProductUpdateForm

    def get_queryset(self):
        return ProductDAO.get_products_list(include_price=True, include_image=False)

    def get_success_url(self):
        return reverse('update product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['default_product_image'] = DEFAULT_PRODUCT_IMAGE
        return context

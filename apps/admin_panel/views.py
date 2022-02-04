from django.views.generic import CreateView, ListView

from apps.admin_panel.forms import AddProductForm
from services.product_service import ProductManager


class ProductAddView(CreateView):
    """
    View is used for products creation via admin panel
    """
    template_name = 'admin_panel/add_product.html'
    form_class = AddProductForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProductsListAdminView(ListView):
    template_name = 'admin_panel/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = ProductManager().get_products_list
        return queryset.values('id', 'image', 'name', 'price', 'amount', 'vendor', 'category', 'date_created')
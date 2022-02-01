from django.views.generic import CreateView, TemplateView

from apps.store.forms import AddProductForm


class ProductAddView(CreateView):
    template_name = 'add_product.html'
    form_class = AddProductForm


class IndexView(TemplateView):
    template_name = 'index.html'

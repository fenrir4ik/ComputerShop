from django.views.generic import CreateView, TemplateView

from apps.store.forms import AddProductForm


class ProductAddView(CreateView):
    template_name = 'add_product.html'
    form_class = AddProductForm
    success_url = 'add-product/'

    def form_invalid(self, form):
        print(form.image_formset.is_valid())
        return super(ProductAddView, self).form_invalid(form)


class IndexView(TemplateView):
    template_name = 'index.html'

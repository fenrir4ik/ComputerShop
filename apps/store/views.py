from django.views.generic import CreateView, TemplateView

from apps.store.forms import AddProductForm


class ProductAddView(CreateView):
    template_name = 'add_product.html'
    form_class = AddProductForm
    success_url = 'add-product/'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class IndexView(TemplateView):
    template_name = 'index.html'

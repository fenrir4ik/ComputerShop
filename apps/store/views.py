from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from apps.store.forms import AddProductToCartForm
from services.dao.image_dao import ImageDao
from services.dao.product_dao import ProductDAO


class IndexView(ListView):
    template_name = 'store/index.html'
    context_object_name = 'products'

    # paginate_by = 20

    def get_queryset(self):
        # amount and date_created not used
        queryset = ProductDAO.get_products_list()
        return queryset.values('id', 'image', 'name', 'price', 'amount', 'date_created')


class ProductDetailView(FormMixin, DetailView):
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    form_class = AddProductToCartForm

    def get_queryset(self):
        queryset = ProductDAO.get_products_list(include_image=False)
        return queryset.values('id', 'name', 'price', 'description', 'amount')

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product_images'] = ImageDao.get_product_images(self.object.get('id'))
        context['form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['max_amount'] = self.object.get('amount')
        return kwargs

    def get_success_url(self):
        return reverse('product detail', kwargs={'pk': self.object.get('id')})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product_amount = form.cleaned_data.get('amount')
        product_id = self.object.get('id')
        print(f'User {self.request.user.pk} adds {product_amount} items of product {product_id} to cart')
        # call process product_amount, product_id
        # THINK TO CREATE SEPARATE FORM FOR UPDATE !! WARNING
        return super().form_valid(form)

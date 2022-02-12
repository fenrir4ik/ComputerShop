from django.views import View
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from apps.store.forms import AddProductToCartForm
from apps.store.models import Product
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


class SingleProductView(DetailView):
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = ProductDAO.get_products_list(include_image=False)
        return queryset.values('id', 'name', 'price', 'description', 'amount')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ImageDao.get_product_images(self.object.get('id'))
        context['form'] = AddProductToCartForm(max_amount=self.object.get('amount'))
        return context


class SingleProductFormView(SingleObjectMixin, FormView):
    template_name = 'store/product_detail.html'
    form_class = AddProductToCartForm

    def get_queryset(self):
        return Product.objects.values('id', 'amount')

    def get_success_url(self):
        return self.request.path_info

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['max_amount'] = self.object.get('amount')
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        product_amount = form.cleaned_data.get('amount')
        product_id = self.object.get('id')
        print(f'User {self.request.user.pk} adds {product_amount} items of product {product_id} to cart')
        # Call process product_amount, product_id
        return super().form_valid(form)


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        view = SingleProductView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)

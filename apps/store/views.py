from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from apps.store.forms import AddProductToCartForm
from apps.store.models import Product
from services.cart_service import CartService
from services.dao.cart_item_dao import CartItemDAO
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
        product_amount = self.object.get('amount')
        product_id = self.object.get('id')
        user_id = self.request.user.pk

        context['product_amount_in_cart'] = CartItemDAO.get_product_amount_in_cart_by_user_id(user_id, product_id)
        context['form'] = AddProductToCartForm(max_amount=product_amount + context['product_amount_in_cart'])
        context['product_images'] = ImageDao.get_product_images(product_id)
        return context


class SingleProductFormView(SingleObjectMixin, FormView):
    form_class = AddProductToCartForm

    def get_queryset(self):
        return Product.objects.values('id', 'amount')

    def get_success_url(self):
        return self.request.path_info

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['max_amount'] = CartItemDAO.get_product_amount_in_cart_by_user_id(
            self.request.user.pk,
            self.object.get('id')
        ) + self.object.get('amount')
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        product_amount = form.cleaned_data.get('amount')
        product_id = self.object.get('id')
        service = CartService()
        service.process_cart_item(self.request.user.pk, product_id, product_amount)
        return super().form_valid(form)


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        view = SingleProductView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)


class ProductDeleteFromCartView(View):
    def post(self, request, *args, **kwargs):
        service = CartService()
        service.delete_product_from_cart(request.user.pk, kwargs.get('pk'))
        next_page = request.GET.get('next')
        return redirect(next_page) if next_page else reverse('index')

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
        max_amount = self.object.get('amount') + \
                     CartItemDAO.get_product_amount_in_cart(
                         self.request.user.pk,
                         self.object.get('id')
                     )
        context['form'] = AddProductToCartForm(max_amount=max_amount)
        return context


class SingleProductFormView(SingleObjectMixin, FormView):
    template_name = 'store/product_detail.html'
    form_class = AddProductToCartForm

    def get_queryset(self):
        return Product.objects.values('id', 'amount')

    def get_success_url(self):
        return self.request.path_info

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['product_images'] = ImageDao.get_product_images(self.object.get('id'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['max_amount'] = self.object.get('amount') + \
                               CartItemDAO.get_product_amount_in_cart(
                                   self.request.user.pk,
                                   self.object.get('id')
                               )
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


class ProductDetailView(SingleObjectMixin, View):
    # WARNING SILK A LOT OF REQUESTS 9 (ORDER AND CART_ITEM DUPLICATES) WHEN CALCULATING MAX AMOUNT + \ {}
    def get(self, request, *args, **kwargs):
        view = SingleProductView.as_view(extra_context=self.get_extra_context())
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SingleProductFormView.as_view(extra_context=self.get_extra_context())
        return view(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ProductDAO.get_products_list(include_image=False)
        return queryset.values('id', 'name', 'price', 'description', 'amount')

    def get_extra_context(self):
        extra_context = {}

        self.object = self.get_object()
        product_id = self.object.get('id')
        user_id = self.request.user.pk

        extra_context['product_images'] = ImageDao.get_product_images(product_id)
        extra_context['product_amount_in_cart'] = CartItemDAO.get_product_amount_in_cart(user_id, product_id)
        return extra_context


class ProductDeleteFromCartView(View):
    def post(self, request, *args, **kwargs):
        service = CartService()
        service.delete_product_from_cart(request.user.pk, kwargs.get('pk'))
        next_page = request.GET.get('next')
        return redirect(next_page) if next_page else reverse('index')

from django.db.models import Sum, F
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView

from apps.core.permissions import CustomerPermission
from apps.store.filters import ProductFilter, OrderFilter
from apps.store.forms import AddProductToCartForm, CreateOrderForm
from apps.store.models import Product
from db.cart_item_dao import CartItemDAO
from db.image_dao import ImageDAO
from db.order_dao import OrderDAO
from db.product_dao import ProductDAO
from services.cart_service import CartService
from services.product_service import ProductPriceHistoryService


class IndexView(ListView):
    """View is used for main page"""
    template_name = 'store/index.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET)
        return context

    def get_queryset(self):
        # amount and date_created not used
        queryset = ProductDAO.get_products_list()
        queryset = queryset.values('id', 'image', 'name', 'price', 'amount', 'date_created')
        queryset = queryset.order_by('-id')
        filter = ProductFilter(self.request.GET, queryset=queryset)
        return filter.qs


class SingleProductView(DetailView):
    """View is used for displaying product detail page with form"""
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = ProductDAO.get_products_list(include_image=False)
        return queryset.values('id', 'name', 'price', 'description', 'amount')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.object.get('id')

        context['product_images'] = ImageDAO.get_product_images(product_id)
        context['product_price_history'] = ProductPriceHistoryService.get_product_price_history(product_id)

        if self.request.user.is_authenticated:
            product_amount = self.object.get('amount')
            user_id = self.request.user.pk
            context['product_amount_in_cart'] = CartItemDAO.get_product_amount_in_cart_by_user_id(user_id, product_id)
            context['form'] = AddProductToCartForm(amount_in_cart=context['product_amount_in_cart'],
                                                   max_amount=product_amount + context['product_amount_in_cart'])
        return context


class SingleProductFormView(CustomerPermission, SingleObjectMixin, FormView):
    """View is used for processing submitted data on product detail page"""
    form_class = AddProductToCartForm

    def get_queryset(self):
        return Product.objects.values('id', 'amount')

    def get_success_url(self):
        return self.request.path_info

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['amount_in_cart'] = CartItemDAO.get_product_amount_in_cart_by_user_id(
            self.request.user.pk,
            self.object.get('id')
        )
        kwargs['max_amount'] = kwargs['amount_in_cart'] + self.object.get('amount')
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return redirect(self.get_success_url())

    def form_valid(self, form):
        product_amount = form.cleaned_data.get('amount')
        product_id = self.object.get('id')
        cart_service = CartService(self.request.user.pk)
        cart_service.process_cart_item(product_id, product_amount)
        return super().form_valid(form)


class ProductDetailView(View):
    """View is used for working with product detail page (both POST and GET)"""

    def get(self, request, *args, **kwargs):
        view = SingleProductView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)


class ProductDeleteFromCartView(CustomerPermission, View):
    """View is used for deletion product from cart"""

    def post(self, request, *args, **kwargs):
        cart_service = CartService(request.user.pk)
        cart_service.delete_product_from_cart(kwargs.get('pk'))
        next_page = request.GET.get('next')
        return redirect(next_page) if next_page else reverse('index')


class UserCartView(CustomerPermission, ListView):
    """View is used for displaying user cart"""
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItemDAO.get_user_cart(self.request.user.pk) \
            .values('amount', 'product_id', 'product__name', 'image', 'price', 'product__amount') \
            .order_by('-product_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = context.get('cart_items').aggregate(total = Sum(F('amount')*F('price'))).get('total')
        return context

    def post(self, request, *args, **kwargs):
        kwargs['pk'] = request.POST.get('pk')
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)


class OrderCreateView(CustomerPermission, CreateView):
    """View is used for checkout"""
    template_name = 'store/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user-orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItemDAO.get_user_cart(self.request.user.pk) \
            .values('amount', 'product_id', 'product__name', 'image', 'price') \
            .order_by('-product_id')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserOrdersListView(CustomerPermission, ListView):
    """View is used for displaying own user orders"""
    template_name = 'store/user_orders.html'
    context_object_name = 'orders_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = OrderFilter(self.request.GET)
        return context

    def get_queryset(self):
        queryset = OrderDAO.get_all_orders(self.request.user.pk)
        queryset = queryset.order_by('-id')
        filter = OrderFilter(self.request.GET, queryset=queryset)
        return filter.qs

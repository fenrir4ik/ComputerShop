from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView

from apps.store.forms import AddProductToCartForm, CreateOrderForm
from apps.store.models import Product
from services.cart_service import CartService
from services.dao.cart_item_dao import CartItemDAO
from services.dao.image_dao import ImageDao
from services.dao.order_dao import OrderDAO
from services.dao.product_dao import ProductDAO


class IndexView(ListView):
    """
    View is used for main page
    """
    template_name = 'store/index.html'
    context_object_name = 'products'

    # paginate_by = 20

    def get_queryset(self):
        # amount and date_created not used
        queryset = ProductDAO.get_products_list()
        return queryset.values('id', 'image', 'name', 'price', 'amount', 'date_created')


class SingleProductView(DetailView):
    """
    View is used for displaying product detail page with form
    """
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
        context['form'] = AddProductToCartForm(amount_in_cart=context['product_amount_in_cart'],
                                               max_amount=product_amount + context['product_amount_in_cart'])
        context['product_images'] = ImageDao.get_product_images(product_id)
        return context


class SingleProductFormView(SingleObjectMixin, FormView):
    """
    View is used for processing submitted data on product detail page
    """
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
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        product_amount = form.cleaned_data.get('amount')
        product_id = self.object.get('id')
        service = CartService()
        service.process_cart_item(self.request.user.pk, product_id, product_amount)
        return super().form_valid(form)


class ProductDetailView(View):
    """
    View is used for working with product detail page (both POST and GET)
    """

    def get(self, request, *args, **kwargs):
        view = SingleProductView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)


class ProductDeleteFromCartView(View):
    """
    View is used for deletion product from cart
    """
    def post(self, request, *args, **kwargs):
        service = CartService()
        service.delete_product_from_cart(request.user.pk, kwargs.get('pk'))
        next_page = request.GET.get('next')
        return redirect(next_page) if next_page else reverse('index')


class UserCartView(ListView):
    """
    View is used for displaying user cart
    """
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItemDAO.get_user_cart(self.request.user.pk) \
            .values('amount', 'product_id', 'product__name', 'image', 'price', 'product__amount') \
            .order_by('-product_id')

    def post(self, request, *args, **kwargs):
        kwargs['pk'] = request.POST.get('pk')
        view = SingleProductFormView.as_view()
        return view(request, *args, **kwargs)


class UserCartClearView(TemplateView):
    """
    View is used for shopping cart clearing
    """
    template_name = 'store/cart_clear.html'

    def post(self, request, *args, **kwargs):
        service = CartService()
        service.clear_user_cart(request.user.pk)
        return redirect('user-cart')


class OrderCreateView(CreateView):
    """
    View is used for checkout
    """
    template_name = 'store/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user-orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_items'] = CartItemDAO.get_user_cart(self.request.user.pk) \
            .values('amount', 'product_id', 'product__name', 'image', 'price', 'product__amount') \
            .order_by('-product_id')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserOrdersListView(ListView):
    """
    View is used for displaying own user orders
    """
    template_name = 'store/user_orders.html'
    context_object_name = 'orders_list'

    def get_queryset(self):
        return OrderDAO.get_all_orders(self.request.user.pk)


class UserOrderDetailView(DetailView):
    """
    View is used for displaying single order from user orders list
    """
    template_name = 'store/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return OrderDAO.get_all_orders(self.request.user.pk)

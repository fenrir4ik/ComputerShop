import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SearchForm, ProductAmountForm, CheckoutForm
from ..accounts.cookie_manager import CookieManager
from ..api.utils import create_api_request_url


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_request = form.cleaned_data['search_request']
            url = create_api_request_url(request, reverse('Product API:Product List'))
            product_response = requests.get(url, {'search': search_request})
        else:
            product_response = None
    else:
        form = SearchForm()
        filter_data = {'page': request.GET.get('page', '1'),
                       'product_type': request.GET.get('product_type', ''),
                       'ordering': request.GET.get('ordering', '')}
        url = create_api_request_url(request, reverse('Product API:Product List'))
        product_response = requests.get(url, filter_data)

    if product_response and product_response.status_code == 200:
        products = product_response.json()
        if products.get('next'):
            products['next'] = products['next'].split('/')[-1]
        if products.get('previous'):
            products['previous'] = products['previous'].split('/')[-1]
    else:
        products = None

    url = create_api_request_url(request, reverse('Product API:Product Types'))
    product_types_response = requests.get(url)
    product_types = product_types_response.json() if product_types_response.status_code == 200 else None
    return render(request, 'index.html', {'form': form,
                                          'products': products,
                                          'current_page': int(request.GET.get('page', '1')),
                                          'product_types': product_types})


def product_details(request, pk):
    current_amount = 0
    if request.user.is_authenticated:
        url = create_api_request_url(request, reverse('Shopping Cart API:Cart'))
        credentials = CookieManager.get_auth_credentials(request)

        if request.method == 'POST':
            form = ProductAmountForm(request.POST)
            if form.is_valid():
                product_amount = form.cleaned_data.get('product_amount')
                requests.post(url, {"amount": product_amount, "product": pk}, **credentials)

        response = requests.get(url, **credentials)
        if response.status_code == 200:
            current_amount = next((cart_row['amount'] for cart_row in response.json() if cart_row['product']['id'] == pk), 0)

    form = ProductAmountForm()
    url = create_api_request_url(request, reverse('Product API:Product Details', kwargs={'pk': pk}))
    product_response = requests.get(url)
    if product_response.status_code == 200:
        product = product_response.json()
        return render(request, 'product_details.html', {'form': form, 'product': product,
                                                        'current_amount': current_amount})
    else:
        return HttpResponseNotFound()


@login_required
def product_remove(request, pk):
    url = create_api_request_url(request, reverse('Shopping Cart API:Remove Product From Cart', kwargs={'pk': pk}))
    credentials = CookieManager.get_auth_credentials(request)
    requests.delete(url, **credentials)
    next_url = request.GET.get('next')
    return HttpResponseRedirect(next_url)


@login_required
def shopping_cart(request):
    url = create_api_request_url(request, reverse('Shopping Cart API:Cart'))
    credentials = CookieManager.get_auth_credentials(request)
    response = requests.get(url, **credentials)
    if response.status_code == 200:
        cart = response.json()
        cart_total = 0
        for cart_item in cart:
            cart_total += int(cart_item['amount']) * float(cart_item['product']['product_price'])
        return render(request, 'shopping_cart.html', {'cart': cart, 'cart_total': cart_total})
    else:
        return HttpResponseNotFound()


@login_required
def checkout(request):
    url = create_api_request_url(request, reverse('Order API:Payment Types'))
    response = requests.get(url)
    payment_types = response.json() if response.status_code == 200 else None
    payment_types = [(p['id'], p['type']) for p in payment_types]
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        form.fields['payment_type'].choices = payment_types
        if form.is_valid():
            order_data = form.cleaned_data
            url = create_api_request_url(request, reverse('Order API:Order List'))
            credentials = CookieManager.get_auth_credentials(request)
            response = requests.post(url, order_data, **credentials)
            if response.status_code == 200:
                return redirect('orders')
            else:
                form.add_error(None, 'Internal error')
    else:
        form = CheckoutForm()
        form.fields['payment_type'].choices = payment_types
    return render(request, 'checkout.html', {'form': form})


@login_required
def clear_cart(request):
    url = create_api_request_url(request, reverse('Shopping Cart API:Clear Cart'))
    credentials = CookieManager.get_auth_credentials(request)
    requests.delete(url, **credentials)
    next_url = request.GET.get('next')
    return HttpResponseRedirect(next_url)
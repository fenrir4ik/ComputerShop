import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.accounts.cookie_manager import CookieManager
from apps.api.utils import create_api_request_url
from apps.orders.forms import OrderDetailsForm, StatusForm


@login_required
def orders_list(request):
    filter_data = {'page': request.GET.get('page', '1'),
                   'order_status': request.GET.get('order_status', ''),
                   'ordering': request.GET.get('ordering', '')}

    url = create_api_request_url(request, reverse('Order API:Order List'))
    credentials = CookieManager.get_auth_credentials(request)
    order_response = requests.get(url, filter_data, **credentials)

    if order_response.status_code == 200:
        orders = order_response.json()
        if orders.get('next'):
            orders['next'] = orders['next'].split('/')[-1]
        if orders.get('previous'):
            orders['previous'] = orders['previous'].split('/')[-1]
    else:
        orders = None
    url = create_api_request_url(request, reverse('Order API:Orders Status'))
    orders_status_response = requests.get(url)
    orders_status = orders_status_response.json() if orders_status_response.status_code == 200 else None
    return render(request, 'orders.html', {'orders': orders,
                                           'current_page': int(request.GET.get('page', '1')),
                                           'orders_status': orders_status})


@login_required
def order_details(request, pk):
    credentials = CookieManager.get_auth_credentials(request)

    url = create_api_request_url(request, reverse('Order API:Order Details', kwargs={'pk': pk}))
    order_response = requests.get(url, **credentials)
    if order_response.status_code == 200:
        order_data = order_response.json()
    else:
        return HttpResponseNotFound()
    status_is_new = order_data['order_status'] == 'Новый'

    url = create_api_request_url(request, reverse('Order API:Payment Types'))
    payment_response = requests.get(url, **credentials)
    payment_types = payment_response.json() if payment_response.status_code == 200 else None
    payment_types = [(p['id'], p['type']) for p in payment_types]

    url = create_api_request_url(request, reverse('Order API:Orders Status'))
    orders_status_response = requests.get(url, **credentials)
    orders_status = orders_status_response.json() if orders_status_response.status_code == 200 else None
    orders_status = [(s['id'], s['status_name']) for s in orders_status if s['status_name']]

    if not status_is_new:
        orders_status = list(filter(lambda x: x[1] != 'Новый', orders_status))

    if request.method == 'POST':
        if status_is_new:
            form = OrderDetailsForm(request.POST)
            form.fields['payment_type'].choices = payment_types
        else:
            form = StatusForm(request.POST)
        form.fields['order_status'].choices = orders_status
        if form.is_valid():
            updated_order_data = form.cleaned_data
            url = create_api_request_url(request, reverse('Order API:Order Details', kwargs={'pk': pk}))
            requests.patch(url, updated_order_data, **credentials)
            return redirect('order details', pk)
        else:
            if status_is_new:
                form.fields['order_date'].initial = order_data['order_date']
    else:
        form = OrderDetailsForm(initial=order_data)
        form.fields['payment_type'].choices = payment_types
        form.fields['order_status'].choices = orders_status

    url = create_api_request_url(request, reverse('Shopping Cart API:Get Order Cart', kwargs={'pk': pk}))
    order_cart_response = requests.get(url, **credentials)
    order_cart = order_cart_response.json() if order_cart_response.status_code == 200 else None
    cart_total = 0
    for cart_item in order_cart:
        cart_total += int(cart_item['amount']) * float(cart_item['product']['product_price'])

    return render(request, 'order_details.html', {'form': form,
                                                  'order_cart': order_cart,
                                                  'cart_total': cart_total,
                                                  'pk': pk,
                                                  'current_payment': order_data['payment_type'],
                                                  'current_status': order_data['order_status']})

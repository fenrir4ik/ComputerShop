import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from apps.accounts.cookie_manager import CookieManager
from apps.api.utils import create_api_request_url


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
def order_details(request):
    pass
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import SearchForm
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


def details(request, pk):
    return HttpResponse(pk)

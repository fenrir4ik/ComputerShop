from urllib.parse import urlencode

import requests
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.accounts.cookie_manager import CookieManager
from apps.api.utils import create_api_request_url
from apps.products.forms import ProductForm


@login_required
@permission_required('is_superuser', raise_exception=True)
def add(request):
    url = create_api_request_url(request, reverse('Product API:Product Vendors'))
    product_vendors = requests.get(url)
    product_vendors = product_vendors.json() if product_vendors.status_code == 200 else None
    product_vendors = [(v['id'], v['vendor_name']) for v in product_vendors]

    url = create_api_request_url(request, reverse('Product API:Product Types'))
    product_types = requests.get(url)
    product_types = product_types.json() if product_types.status_code == 200 else None
    product_types = [(pt['id'], pt['type_name']) for pt in product_types]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.fields['product_type'].choices = product_types
        form.fields['product_vendor'].choices = product_vendors
        if form.is_valid():
            product_data = form.cleaned_data
            credentials = CookieManager.get_auth_credentials(request)
            url = create_api_request_url(request, reverse('Product API:Product List'))
            product_image = product_data.pop('product_image')
            add_product_response = requests.post(url, product_data, files={'product_image': product_image},
                                                 **credentials)
            if add_product_response.status_code == 201:
                form = ProductForm()
                form.fields['product_type'].choices = product_types
                form.fields['product_vendor'].choices = product_vendors
                return render(request, 'product_update.html', {'form': form,
                                                               'product_id': add_product_response.json().get('id')})
            else:
                form.add_error(None, add_product_response.json())
    else:
        form = ProductForm()
        form.fields['product_type'].choices = product_types
        form.fields['product_vendor'].choices = product_vendors
    return render(request, 'product_update.html', {'form': form})


@login_required
@permission_required('is_superuser', raise_exception=True)
def edit(request, pk):
    url = create_api_request_url(request, reverse('Product API:Product Vendors'))
    product_vendors = requests.get(url)
    product_vendors = product_vendors.json() if product_vendors.status_code == 200 else None
    product_vendors = [(v['id'], v['vendor_name']) for v in product_vendors]

    url = create_api_request_url(request, reverse('Product API:Product Types'))
    product_types = requests.get(url)
    product_types = product_types.json() if product_types.status_code == 200 else None
    product_types = [(pt['id'], pt['type_name']) for pt in product_types]
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.fields['product_type'].choices = product_types
        form.fields['product_vendor'].choices = product_vendors
        if form.is_valid():
            product_data = form.cleaned_data
            product_image = product_data.pop('product_image')
            credentials = CookieManager.get_auth_credentials(request)
            url = create_api_request_url(request, reverse('Product API:Product Details', kwargs={'pk': pk}))
            product_update_response = requests.put(url, product_data, files={'product_image': product_image},
                                                   **credentials)
            return render(request, 'product_update.html', {'pk': pk,
                                                           'form': form,
                                                           'product_id': product_update_response.json().get('id')})
    else:
        url = create_api_request_url(request, reverse('Product API:Product Details', kwargs={'pk': pk}))
        product_details = requests.get(url)
        if product_details.status_code == 200:
            product_details = product_details.json()
        else:
            return HttpResponseNotFound()
        form = ProductForm(initial=product_details)
        form.fields['product_type'].choices = product_types
        form.fields['product_vendor'].choices = product_vendors
    return render(request, 'product_update.html', {'pk': pk,
                                                   'form': form})


@login_required
@permission_required('is_superuser', raise_exception=True)
def delete(request, pk):
    url = create_api_request_url(request, reverse('Product API:Product Details', kwargs={'pk': pk}))
    credentials = CookieManager.get_auth_credentials(request)
    product_delete_response = requests.delete(url, **credentials)
    if product_delete_response.status_code == 200:
        return redirect('index')
    else:
        deleted_info = urlencode({'not_deleted': True})
        return redirect(f"{reverse('edit product', kwargs={'pk': pk})}?{deleted_info}")

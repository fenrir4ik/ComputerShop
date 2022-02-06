from django.views.generic import ListView

from services import product_services


class IndexView(ListView):
    template_name = 'store/index.html'
    context_object_name = 'products'
    # paginate_by = 20

    def get_queryset(self):
        # amount and date_created not used
        queryset = product_services.ProductRetrieveService().get_products_list()
        return queryset.values('id', 'image', 'name', 'price', 'amount', 'date_created')
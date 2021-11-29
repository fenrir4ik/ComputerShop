import django_filters

from .models import Order, OrderStatus


class OrderFilter(django_filters.FilterSet):
    order_status = django_filters.ModelChoiceFilter(queryset=OrderStatus.objects.all())
    order_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['order_status', 'order_date']

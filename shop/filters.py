import django_filters
from .models import Product


class ProductFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Product
        fields = {
            'unit_price': ['lte', 'gte']
        }
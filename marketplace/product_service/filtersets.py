import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    display_on_main_page = django_filters.BooleanFilter(field_name='display_on_main_page')

    class Meta:
        model = Product
        fields = ['display_on_main_page']

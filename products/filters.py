import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Min Price"
    )
    price_max = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Max Price"
    )

    class Meta:
        model = Product
        fields = ["category", "price_min", "price_max", "available"]

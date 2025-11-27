import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Search"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="All categories"
    )
    min_price = django_filters.NumberFilter(
    field_name="price",
    lookup_expr="gte",
    label="Min price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Max price"
    )
    available = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget(),
        label="In stock"
    )

    class Meta:
        model = Product
        fields = ["search", "category", "min_price", "max_price", "available"]

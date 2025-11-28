import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = django_filters.ChoiceFilter(field_name="category__slug",
                                            label="Category")

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    available = django_filters.BooleanFilter(widget=
                                             django_filters.widgets.BooleanWidget())

    class Meta:
        model = Product
        fields = ["search", "category", "min_price", "max_price", "available"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["category"].extra["choices"] = [(c.slug, c.name) for c in
                                                     Category.objects.all()]

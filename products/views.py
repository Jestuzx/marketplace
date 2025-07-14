from django.views.generic import ListView
from django_filters.views import FilterView
from .models import Product
from .filters import ProductFilter

class ProductListView(FilterView, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'
    filterset_class = ProductFilter
    paginate_by = 10

from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from .models import Product, Category
from .filters import ProductFilter

# Список товаров
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()

        # Фильтр
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs

        # Сортировка
        sort = self.request.GET.get("sort")
        sort_options = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "name",
            "name_desc": "-name",
            "newest": "-created_at",
            "oldest": "created_at",
        }
        if sort in sort_options:
            queryset = queryset.order_by(sort_options[sort])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        context["categories"] = Category.objects.all()
        return context

class ProductSortPartialView(View):
    template_name = "products/partials/product_list_items.html"

    def get(self, request):
        products = Product.objects.all()

        # Фильтр по GET-параметрам
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs

        # Сортировка
        sort = request.GET.get("sort")
        sort_options = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "name",
            "name_desc": "-name",
            "newest": "-created_at",
            "oldest": "created_at",
        }
        if sort in sort_options:
            products = products.order_by(sort_options[sort])

        return render(request, self.template_name, {"products": products})

# Детальная страница товара
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

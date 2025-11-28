from django.urls import path
from .views import ProductListView, ProductSortPartialView, ProductDetailView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("sort/", ProductSortPartialView.as_view(), name="sort_partial"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]

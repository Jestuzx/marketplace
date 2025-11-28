from django.urls import path
from .views import ProductListView, ProductSortPartialView, ProductDetailView
from . import views
app_name = "products"


urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("category/<slug:slug>/", views.CategoryProductsView.as_view(),
          name="category"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("sort_partial/", views.ProductSortPartialView.as_view(), name="sort_partial"),
]

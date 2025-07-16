from django.urls import path
from .views import ProductListView, ProductCreateView, CategoryCreateView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('seller/add/', ProductCreateView.as_view(), name='product_add'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]

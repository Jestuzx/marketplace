from django.urls import path
from .views import (
    CreateOrderView,
    OrderDetailView,
    CartView,
    UpdateCartView,
    add_to_cart,
)

app_name = "orders"

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create_order"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/update/<int:product_id>/", UpdateCartView.as_view(), name="update_cart"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
]

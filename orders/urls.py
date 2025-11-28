from django.urls import path
from .views import (
    CreateOrderView,
    CartView,
    UpdateCartView,
    add_to_cart,
)

app_name = "orders"

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", UpdateCartView.as_view(), name="update_cart"),
    path("create/", CreateOrderView.as_view(), name="create_order"),
]

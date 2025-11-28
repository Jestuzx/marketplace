from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Product
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(View):
    def get(self, request):
        cart = request.session.get("cart", {})
        products = Product.objects.filter(id__in=cart.keys())
        total = sum(p.price * cart.get(str(p.id), 0) for p in products)
        return render(request, "orders/cart.html", {"products": products,
                                                    "cart": cart, "total": total})


class UpdateCartView(View):
    def post(self, request, product_id):
        action = request.POST.get("action")
        cart = request.session.get("cart", {})

        if action == "add":
            cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        elif action == "remove":
            if str(product_id) in cart:
                cart[str(product_id)] -= 1
                if cart[str(product_id)] <= 0:
                    del cart[str(product_id)]
        elif action == "delete":
            if str(product_id) in cart:
                del cart[str(product_id)]

        request.session["cart"] = cart
        return redirect("orders:create_order")


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session["cart"] = cart
    return redirect("orders:create_order")


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get("cart", {})
        products = Product.objects.filter(id__in=cart.keys())
        total = sum(p.price * cart.get(str(p.id), 0) for p in products)
        return render(request, "orders/create_order.html",
                      {"products": products, "cart": cart, "total": total})

    def post(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            return redirect("products:product_list")

        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            buyer=request.user,
            total_price=0,
            address=address,
            phone=phone,
            payment_method=payment_method
        )

        total_price = 0
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            price = product.price * qty
            OrderItem.objects.create(order=order, product=product,
                                      quantity=qty, price=price)
            total_price += price

        order.total_price = total_price
        order.save()

        request.session["cart"] = {}
        return redirect("orders:order_detail", pk=order.pk)

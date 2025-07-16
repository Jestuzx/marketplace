from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from .models import Order, OrderItem, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse



class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        total = sum(p.price * cart[str(p.id)] for p in products)
        return render(request, 'orders/create_order.html', {'products': products, 'cart': cart, 'total': total})

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('products:product_list')

        order = Order.objects.create(buyer=request.user, total_price=0)
        total_price = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_price += price

        order.total_price = total_price
        order.save()

        
        request.session['cart'] = {}

        return redirect('orders:order_detail', pk=order.pk)

class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, buyer=request.user)
        return render(request, 'orders/order_detail.html', {'order': order})

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        return render(request, 'orders/cart.html', {
            'products': products,
            'cart': cart
        })

class UpdateCartView(View):
    def post(self, request, product_id):
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if action == 'add':
            cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        elif action == 'remove':
            if str(product_id) in cart:
                cart[str(product_id)] -= 1
                if cart[str(product_id)] <= 0:
                    del cart[str(product_id)]

        request.session['cart'] = cart

        products = Product.objects.filter(id__in=cart.keys())
        return render(request, 'orders/partials/cart_table.html', {
            'products': products,
            'cart': cart
        })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return render(request, 'orders/partials/cart_count.html', {'cart': cart})

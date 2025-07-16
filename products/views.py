from django.views.generic import ListView, View
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView

from .models import Product, Category
from .filters import ProductFilter
from .forms import ProductForm, CategoryForm

class ProductListView(FilterView, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'
    filterset_class = ProductFilter
    paginate_by = 10

class AddToCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        return redirect('product_list')

class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
        return redirect('orders:create_order')

class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can add products.")
        return super().dispatch(request, *args, **kwargs)

class ProductCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user  # автоматически ставим продавца
        return super().form_valid(form)
    

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:product_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'seller'

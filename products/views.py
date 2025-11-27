from django.views.generic import ListView, View, DetailView
from django_filters.views import FilterView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin
from storages.backends.s3boto3 import S3Boto3Storage
from .models import Product, Category, ProductReview
from .filters import ProductFilter
from .forms import ProductForm, CategoryForm, ProductReviewForm
from django.core.files.storage import default_storage

class ProductListView(FilterView, ListView):
    model = Product
    context_object_name = "products"
    template_name = "products/product_list.html"
    filterset_class = ProductFilter
    paginate_by = 10

class AddToCartView(View):
    def post(self, request, product_id):
        cart = request.session.get("cart", {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session["cart"] = cart
        return redirect("product_list")

class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = request.session.get("cart", {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session["cart"] = cart
        return redirect("orders:create_order")

class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != "seller":
            raise PermissionDenied("Only sellers can add products.")
        return super().dispatch(request, *args, **kwargs)

class ProductCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:product_list")

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.user_type == "seller"
        )

class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    form_class = ProductReviewForm
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            existing_review = ProductReview.objects.get(
                product=self.get_object(), user=self.request.user
            )
            kwargs["instance"] = existing_review
        except ProductReview.DoesNotExist:
            pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.object.reviews.all()
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        review_form = self.get_form()
        product_form = ProductForm(request.POST, request.FILES, instance=self.object)

        # Сохраняем отзыв
        if review_form.is_valid():
            ProductReview.objects.update_or_create(
                product=self.object,
                user=request.user,
                defaults=review_form.cleaned_data
            )

        if product_form.is_valid():
            s3 = S3Boto3Storage()
            image = product_form.cleaned_data.get("image")
            if image:
                self.object.image.save(image.name, image, save=True, storage=s3)
            else:
                product_form.save()

        return super().form_valid(review_form)
print("Current default storage:", default_storage.__class__)

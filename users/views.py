from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, SellerReviewForm
from .models import CustomUser, SellerReview
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from orders.models import Order  # импортируй модель заказа
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse



class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
            user = form.save(commit=False)
            user.save()
            return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущего пользователя
        user = self.request.user
        # Получаем все его заказы
        context['orders'] = Order.objects.filter(buyer=user).order_by('-created_at')
        return context


class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'seller':
            raise PermissionDenied("You must be a seller to access this page.")
        return super().dispatch(request, *args, **kwargs)

class SellerProfileView(LoginRequiredMixin, FormMixin, DetailView):
    model = CustomUser
    template_name = 'users/seller_profile.html'
    context_object_name = 'seller'
    form_class = SellerReviewForm
    pk_url_kwarg = 'seller_id'

    def get_queryset(self):
        return CustomUser.objects.filter(user_type='seller')

    def get_success_url(self):
        return reverse('users:seller_profile', kwargs={'seller_id': self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            existing_review = SellerReview.objects.get(seller=self.get_object(), buyer=self.request.user)
            kwargs['instance'] = existing_review
        except SellerReview.DoesNotExist:
            pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews_received.all()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review, created = SellerReview.objects.update_or_create(
                seller=self.object,
                buyer=self.request.user,
                defaults=form.cleaned_data
            )
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
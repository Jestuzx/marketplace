from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from orders.models import Order  # импортируй модель заказа
from django.core.exceptions import PermissionDenied


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

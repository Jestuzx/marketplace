from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, SellerReviewForm, UserForm, SellerProfileForm
from .models import CustomUser, SellerReview
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from orders.models import Order 
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import render
from .models import SellerProfile
from .serializers import SellerProfileSerializer
from django.views import View
from django.http import HttpResponse



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

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile, _ = SellerProfile.objects.get_or_create(user=request.user)
        serializer = SellerProfileSerializer(profile)
        return render(request, "users/seller_profile_form.html", {"serializer": serializer, "profile": profile})

    def post(self, request):
        profile, _ = SellerProfile.objects.get_or_create(user=request.user)
        serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        return Response(serializer.errors, status=400)
    
class SellerProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile, _ = SellerProfile.objects.get_or_create(user=request.user)
        serializer = SellerProfileSerializer(profile)
        return render(request, "users/seller_profile_edit.html", {"profile": profile, "serializer": serializer})

    def post(self, request):
        profile, _ = SellerProfile.objects.get_or_create(user=request.user)
        serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        return Response(serializer.errors, status=400)
    
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            seller_profile = user.sellerprofile
        except SellerProfile.DoesNotExist:
            seller_profile = None

        user_form = UserForm(instance=user)
        seller_form = SellerProfileForm(instance=seller_profile)

        return render(request, 'users/profile_edit.html', {
            'user_form': user_form,
            'seller_form': seller_form,
        })

    def post(self, request):
        user = request.user
        try:
            seller_profile = user.sellerprofile
        except SellerProfile.DoesNotExist:
            seller_profile = None

        user_form = UserForm(request.POST, request.FILES, instance=user)
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)

        if user_form.is_valid() and (seller_form is None or seller_form.is_valid()):
            user_form.save()
            if seller_form:
                seller_form.save()

            if request.headers.get('HX-Request'):  # проверяем, запрос от HTMX
                response = HttpResponse()
                response['HX-Redirect'] = reverse('profile')  # редирект для HTMX
                return response
            else:
                return redirect('profile')  # обычный редирект

        return render(request, 'users/profile_edit.html', {
            'user_form': user_form,
            'seller_form': seller_form,
        })
    def get(self, request):
        user = request.user
        try:
            seller_profile = user.sellerprofile
        except SellerProfile.DoesNotExist:
            seller_profile = None

        user_form = UserForm(instance=user)
        seller_form = SellerProfileForm(instance=seller_profile)

        return render(request, 'users/profile_edit.html', {
            'user_form': user_form,
            'seller_form': seller_form,
        })

    def post(self, request):
        user = request.user
        try:
            seller_profile = user.sellerprofile
        except SellerProfile.DoesNotExist:
            seller_profile = None

        user_form = UserForm(request.POST, request.FILES, instance=user)
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)

        if user_form.is_valid() and (seller_form is None or seller_form.is_valid()):
            user_form.save()
            if seller_form:
                seller_form.save()
            return redirect('profile') 

        return render(request, 'users/profile_edit.html', {
            'user_form': user_form,
            'seller_form': seller_form,
        })
    
        
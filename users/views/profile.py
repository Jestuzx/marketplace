from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import UserForm, SellerProfileForm
from ..models import CustomUser, SellerProfile
from orders.models import Order
from django.http import HttpResponse

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['orders'] = Order.objects.filter(buyer=user).order_by('-created_at')
        return context


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'users/profile_edit.html'

    def get(self, request):
        user = request.user
        try:
            seller_profile = user.sellerprofile
        except SellerProfile.DoesNotExist:
            seller_profile = None

        user_form = UserForm(instance=user)
        seller_form = SellerProfileForm(instance=seller_profile)

        return render(request, self.template_name, {
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

            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = reverse('profile')
                return response
            else:
                return redirect('profile')

        return render(request, self.template_name, {
            'user_form': user_form,
            'seller_form': seller_form,
        })

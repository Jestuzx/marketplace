from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from ..forms import UserForm, SellerProfileForm
from orders.models import Order
from ..mixins import SellerProfileMixin



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(
            buyer=self.request.user
        ).order_by("-created_at")
        return context


class ProfileEditView(LoginRequiredMixin, SellerProfileMixin, UpdateView):
    template_name = "users/profile_edit.html"
    form_class = UserForm
    seller_form_class = SellerProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_form"] = context.get("form") or self.form_class(
            instance=self.request.user
        )

        context["seller_form"] = self.seller_form_class(
            instance=self.get_seller_profile(self.request.user)
        )

        return context

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(
            request.POST,
            request.FILES,
            instance=self.get_object()
        )
        return self.handle_forms(request, user_form, self.template_name)

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import SellerProfile
from rest_framework.response import Response

class SellerProfileMixin:
    seller_form_class = None

    def get_seller_profile(self, user):
        return SellerProfile.objects.get_or_create(user=user)[0]

    def get_seller_form(self, request, instance=None):
        if not self.seller_form_class:
            return None
        return self.seller_form_class(request.POST or None, request.FILES or None
                                      , instance=instance)

    def handle_forms(self, request, main_form, template_name):
        seller_form = self.get_seller_form(request,
                                           instance=self.get_seller_profile(request.user))

        if main_form.is_valid() and (seller_form is None or seller_form.is_valid()):
            main_form.save()
            if seller_form:
                seller_form.save()

            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response["HX-Redirect"] = reverse("profile")
                return response
            return redirect("profile")

        return render(request, template_name, {"form": main_form,
                                               "seller_form": seller_form})

class SellerProfileDRFMixin:

    serializer_class = None
    template_name = None

    def get_profile(self, user):
        return SellerProfile.objects.get_or_create(user=user)[0]

    def get_serializer(self, instance, data=None, partial=True):
        if not self.serializer_class:
            return None
        return self.serializer_class(instance, data=data, partial=partial)

    def render_form(self, request, serializer, profile):
        return render(request, self.template_name, {"serializer": serializer
                                                    ,"profile": profile})

    def save_profile(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        return Response(serializer.errors, status=400)

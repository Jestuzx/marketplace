from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import render
from ..models import SellerProfile
from ..serializers import SellerProfileSerializer


class BaseSellerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    template_name = None

    def get_profile(self, user):
        profile, _ = SellerProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self.get_profile(request.user)
        serializer = SellerProfileSerializer(profile)
        return render(request, self.template_name,
                       {"serializer": serializer, "profile": profile})

    def post(self, request):
        profile = self.get_profile(request.user)
        serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        return Response(serializer.errors, status=400)


class SellerProfileView(BaseSellerProfileView):
    template_name = "users/seller_profile_form.html"


class SellerProfileEditView(BaseSellerProfileView):
    template_name = "users/seller_profile_edit.html"

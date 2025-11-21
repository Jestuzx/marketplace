from django.urls import path
from .views import (
    AuthView,
    ProfileView,
    ProfileEditView,
    SellerProfileView,
    SellerProfileEditView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("auth/", AuthView.as_view(), name="auth"),
    path("logout/", LogoutView.as_view(next_page="auth"), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("seller/profile/", SellerProfileView.as_view(), name="seller_profile"),
    path(
        "seller/profile/edit/",
        SellerProfileEditView.as_view(),
        name="seller_profile_edit",
    ),
]

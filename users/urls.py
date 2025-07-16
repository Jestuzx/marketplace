from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView, SellerProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('seller/<int:seller_id>/', SellerProfileView.as_view(), name='seller_profile'),
]

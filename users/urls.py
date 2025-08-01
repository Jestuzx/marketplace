from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView, SellerProfileView, ProfileEditView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('seller/<int:seller_id>/', SellerProfileView.as_view(), name='seller_profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerReview, SellerProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "user_type"]


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ["avatar", "store_name", "description", "payment_info"]


class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]

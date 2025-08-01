from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerReview, SellerProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'avatar', 'store_name']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        store_name = cleaned_data.get('store_name')

        if user_type == 'seller' and not store_name:
            self.add_error('store_name', 'Store name is required for sellers.')

        return cleaned_data

class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name'] 

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['avatar', 'store_name', 'description', 'payment_info']

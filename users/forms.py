from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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
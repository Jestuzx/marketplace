from django.contrib import admin
from .models import Category


from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "price", "available", "created_at")
    list_filter = ("available", "created_at", "category")
    search_fields = ("name", "description")

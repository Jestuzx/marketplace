from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SellerProfile

@receiver(post_save, sender=CustomUser)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.is_seller:
        SellerProfile.objects.create(user=instance)

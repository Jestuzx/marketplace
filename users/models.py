from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    store_name = models.CharField(max_length=100, blank=True) 

    @property
    def average_rating(self):
        reviews = self.reviews_received.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def __str__(self):
        return f"{self.username} ({self.user_type})"
    

class SellerReview(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    rating = models.PositiveIntegerField()  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seller', 'buyer')

    def __str__(self):
        return f"{self.buyer.username} → {self.seller.username} ({self.rating})"
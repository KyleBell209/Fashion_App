from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserPreference, Likes

@receiver(post_save, sender=UserPreference)
def remove_mismatched_gender_items(sender, instance, **kwargs):
    preferences = instance
    customer = preferences.customer
    likes, _ = Likes.objects.get_or_create(customer=customer, complete=False)

    for item in likes.likeitem_set.all():
        product_gender = item.product.gender
        if product_gender != preferences.gender and product_gender != "Unisex":
            item.delete()
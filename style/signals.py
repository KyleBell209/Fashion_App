from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserPreference, Likes

# Define a signal receiver function that is triggered when a UserPreference object is saved
@receiver(post_save, sender=UserPreference)
def remove_mismatched_gender_items(sender, instance, **kwargs):
    # Retrieve the preferences and associated account from the saved UserPreference object
    preferences = instance
    account = preferences.account

    # Retrieve the Likes object associated with the account
    likes, _ = Likes.objects.get_or_create(account=account)

    # Loop through each LikeItem object associated with the Likes object
    for item in likes.likeitem_set.all():
        # Check whether the gender of the product associated with the LikeItem object matches the user's gender preference
        product_gender = item.product.gender
        if product_gender != preferences.gender and product_gender != "Unisex":
            # If the gender preference and product gender do not match and the product gender is not "Unisex", delete the LikeItem object
            item.delete()

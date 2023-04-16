from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
import re
# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    preferences = models.OneToOneField('UserPreference', null=True, blank=True, on_delete=models.SET_NULL, related_name='account_preferences')

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user_preference')
    gender = models.CharField(max_length=200, null=True, blank=True)
    masterCategory = models.CharField(max_length=200, null=True, blank=True)
    subCategory = models.CharField(max_length=200, null=True, blank=True)
    articleType = models.CharField(max_length=200, null=True, blank=True)
    baseColour = models.CharField(max_length=200, null=True, blank=True)
    season = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    usage = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.account.name} Preferences'

class FashionProduct(models.Model):
	
	gender = models.CharField(_("gender"),max_length=200)
	masterCategory = models.CharField(_("masterCategory"),max_length=200)
	subCategory = models.CharField(_("subCategory"),max_length=200)
	articleType = models.CharField(_("articleType"),max_length=200)
	baseColour = models.CharField(_("baseColour"),max_length=200)
	season = models.CharField(_("season"),max_length=200)
	year = models.CharField(_("year"),max_length=200)
	usage = models.CharField(_("usage"),max_length=200)
	productDisplayName = models.CharField(_("productDisplayName"),max_length=200)
	imagePath = models.CharField(_("imagePath"),max_length=200)
	
	def __str__(self):
		return self.productDisplayName
	
	@property
	def imageURL(self):
		return f'{settings.MEDIA_URL}{self.imagePath}'

class Likes(models.Model):
	account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_likes_items(self):
		likeitems = self.likeitem_set.all()
		total = sum([item.quantity for item in likeitems])
		return total 

	@property
	def get_likes_product_ids(self):
		likeitems = self.likeitem_set.all()
		product_ids = [item.product.id for item in likeitems]
		return product_ids 

class LikeItem(models.Model):
    product = models.ForeignKey(FashionProduct, on_delete=models.SET_NULL, null=True)
    likes = models.ForeignKey(Likes, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    masterCategory = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    superliked = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.product:
            self.masterCategory = self.product.masterCategory
            self.name = self.product.productDisplayName
        super(LikeItem, self).save(*args, **kwargs)


class RecommendedImage(models.Model):
    product = models.ForeignKey(FashionProduct, on_delete=models.CASCADE, null=True)
    image_url = models.CharField(max_length=500, null=True)
    masterCategory = models.CharField(max_length=200, null=True)
    related_product_masterCategory = models.CharField(max_length=200, null=True) # Add this field

    def __str__(self):
        return f'RecommendedImage for {self.product}'
    
    def get_related_product_name(self):
        match = re.search(r'(?<=/images\\).+?(?=.jpg)', self.image_url)
        if match:
            product_id = int(match.group())
            related_product = FashionProduct.objects.get(id=product_id)
            return related_product.productDisplayName
        else:
            return "Product not found"

    def get_related_product_masterCategory(self):
        match = re.search(r'(?<=/images\\).+?(?=.jpg)', self.image_url)
        if match:
            product_id = int(match.group())
            related_product = FashionProduct.objects.get(id=product_id)
            return related_product.masterCategory
        else:
            return None


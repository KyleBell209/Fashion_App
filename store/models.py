from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    preferences = models.OneToOneField('UserPreference', null=True, blank=True, on_delete=models.SET_NULL, related_name='customer_preferences')

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='user_preference')
    gender = models.CharField(max_length=200, null=True, blank=True)
    masterCategory = models.CharField(max_length=200, null=True, blank=True)
    subCategory = models.CharField(max_length=200, null=True, blank=True)
    articleType = models.CharField(max_length=200, null=True, blank=True)
    baseColour = models.CharField(max_length=200, null=True, blank=True)
    season = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    usage = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.customer.name} Preferences'

class ProductTest(models.Model):
	
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

#comment out class Product below to use ProductTest above


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
    product = models.ForeignKey(ProductTest, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    masterCategory = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        if self.product:
            self.masterCategory = self.product.masterCategory
            self.name = self.product.productDisplayName
        super(OrderItem, self).save(*args, **kwargs)

class RecommendedImage(models.Model):
    product = models.ForeignKey(ProductTest, on_delete=models.CASCADE, null=True)
    image_url = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f'RecommendedImage for {self.product}'


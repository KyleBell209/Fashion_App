from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductTest)
admin.site.register(RecommendedImage)
admin.site.register(UserPreference)

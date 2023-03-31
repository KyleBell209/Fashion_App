from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Likes)
admin.site.register(LikeItem)
admin.site.register(ProductTest)
admin.site.register(RecommendedImage)
admin.site.register(UserPreference)
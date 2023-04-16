from django.contrib import admin

from .models import *

admin.site.register(Account)
admin.site.register(Likes)
admin.site.register(LikeItem)
admin.site.register(FashionProduct)
admin.site.register(RecommendedImage)
admin.site.register(UserPreference)
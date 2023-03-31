from django.urls import path

from . import views
from . import accounts

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('likes/', views.likes, name="likes"),
	path('update_item/', views.updateItem, name="update_item"),
    path('survey/', views.survey, name='survey'),    
	path('login/', accounts.userlogin, name="userlogin"),
    path('register/', accounts.register, name="register"),
    path('logout/', accounts.userlogout, name="userlogout"),
    path('get_filtered_products/', views.get_filtered_products, name='get_filtered_products'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('clear_preferences/', views.clear_preferences, name='clear_preferences'),
]
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .accounts import *
from .models import * 
import os
from django.conf import settings
import re
import random
from numpy.linalg import norm
from .recommendations import get_image_recommendations, get_recommended_products, get_mean_likes_recommendations
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction
import time

@login_required(login_url='userlogin')
def style(request):
    account = request.user.account
    likes, created = Likes.objects.get_or_create(account=account)
    items = likes.likeitem_set.all()
    likesItems = likes.get_likes_items
    items_superliked_status = {item.product_id: item.superliked for item in items}
    product_list = FashionProduct.objects.all()
    user_preferences = request.user.account.preferences
    recommended_products = get_recommended_products(product_list, user_preferences)

    # Get filters from request
    q = request.GET.get('q', '').lower()
    master_category = request.GET.get('master_category', None)
    sub_category = request.GET.get('sub_category', None)

    # Filter products according to the search query, master category, and sub category
    filtered_products = [
        product for product in recommended_products
        if (not q or q in product.productDisplayName.lower()) and
           (not master_category or master_category == product.masterCategory) and
           (not sub_category or sub_category == product.subCategory)
    ]

    # Determine the number of products to show per page
    num_products_per_page = 20
    total_num_products = len(filtered_products)
    remaining_products = total_num_products % num_products_per_page
    if remaining_products == 0:
        num_pages = total_num_products // num_products_per_page
    else:
        num_pages = total_num_products // num_products_per_page + 1

    paginator = Paginator(filtered_products, num_products_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # If this is the last page, adjust the number of products per page to be equal to the remaining products
    if page_obj.number == num_pages and remaining_products != 0:
        paginator = Paginator(filtered_products, remaining_products)
        page_obj = paginator.get_page(page_number)

    likesProductIds = likes.get_likes_product_ids
    context = {'page_obj': page_obj, 'likesItems': likesItems, 'likesProductIds': likesProductIds, 'items_superliked_status': items_superliked_status}
    return render(request, 'style/style.html', context)


@staff_member_required
def delete_product(request, product_id):
    product = FashionProduct.objects.get(id=product_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(product.imageURL))

    # Delete the image file
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete the product from the database
    product.delete()

    messages.success(request, f"Product {product.productDisplayName} has been deleted.")
    return HttpResponseRedirect(reverse('style'))

def filter_products_by_preferences(product_list, preferences):
    filtered_products = product_list

    for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
        value = getattr(preferences, field, None)
        if value:
            filtered_products = filtered_products.filter(**{field: value})
    
    num_products = 6
    if len(filtered_products) > num_products:
        return random.sample(list(filtered_products), num_products)
    else:
        return filtered_products

@login_required(login_url='userlogin')
def survey(request):
    if request.method == 'POST':
        account = request.user.account
        preferences, created = UserPreference.objects.get_or_create(account=account)
        
        # Save previous gender preference
        prev_gender = preferences.gender

        for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
            setattr(preferences, field, request.POST.get(field))
        preferences.save()
        account.preferences = preferences
        account.save()

        # Update likes after saving preferences
        likes, _ = Likes.objects.get_or_create(account=account)        

        return redirect('style')

    product_list = FashionProduct.objects.all()
    user_preferences = request.user.account.preferences
    filtered_products = filter_products_by_preferences(product_list, user_preferences)

    context = {'filtered_products': filtered_products, 'user_preferences': user_preferences}
    return render(request, 'style/survey.html', context)

from django.http import JsonResponse

@login_required(login_url='userlogin')
def clear_preferences(request):
    account = request.user.account
    preferences, created = UserPreference.objects.get_or_create(account=account)
    preferences.gender = ''
    preferences.masterCategory = ''
    preferences.subCategory = ''
    preferences.articleType = ''
    preferences.baseColour = ''
    preferences.season = ''
    preferences.year = ''
    preferences.usage = ''
    preferences.save()
    account.preferences = preferences
    account.save()
    return JsonResponse({'success': True})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        account = user.account
        likes = Likes.objects.filter(account=account)
        like_items = LikeItem.objects.filter(likes__in=likes)
        user_preferences = UserPreference.objects.filter(account=account)

        like_items.delete()
        likes.delete()
        user_preferences.delete()
        account.delete()
        user.delete()
        logout(request)

        messages.success(request, 'User account successfully deleted.')
        return redirect('userlogin')  # Redirect to the login page after deleting the account
    else:  # Handle GET request
        return render(request, 'style/delete_account_confirm.html')

@login_required(login_url='userlogin')
def likes(request):
    account = request.user.account
    likes, created = Likes.objects.get_or_create(account=account)
    items = likes.likeitem_set.all()
    likesItems = likes.get_likes_items
    
    filter_type = request.GET.get('filter', 'articleType')

    items_by_filter = {}
    recommended_images = {}
    product_image_urls = []

    start_time = time.time()

    for item in items:
        items_by_filter.setdefault(getattr(item.product, filter_type), []).append(item)
        recommended_images[str(item.id)] = get_image_recommendations(item.product.id)
        product_image_urls.append(item.product.imageURL)

    user_gender = account.preferences.gender if account.preferences and account.preferences.gender else None

    product_image_weights = [1.5 if item.superliked else 1 for item in items]

    mean_likes_recommendations = get_mean_likes_recommendations(product_image_urls, weights=product_image_weights, gender=user_gender)

    filter_mean_recommendations = {
        filter_value: get_mean_likes_recommendations([item.product.imageURL for item in filter_items],
                                                     weights=[1.5 if item.superliked else 1 for item in filter_items],
                                                     master_category=filter_value if filter_type == 'masterCategory' else None,
                                                     gender=user_gender,
                                                     articleType=filter_value if filter_type == 'articleType' else None,
                                                     subCategory=filter_value if filter_type == 'subCategory' else None)
        for filter_value, filter_items in items_by_filter.items()
    }

    context = {
        'items_by_filter': items_by_filter,
        'filter_type': filter_type,
        'likes': likes,
        'likesItems': likesItems,
        'recommended_images': recommended_images,
        'filter_mean_recommendations': filter_mean_recommendations,
    }

    end_time = time.time()

    print(f"Execution time for entire recommendations: {end_time - start_time} seconds")
    return render(request, 'style/likes.html', context)

@login_required(login_url='userlogin')
def remove_all_likes(request):
    account = request.user.account
    likes, created = Likes.objects.get_or_create(account=account)
    items = likes.likeitem_set.all()
    items.delete()
    messages.success(request, 'Likes cleared')
    return redirect('likes')

def get_filtered_products(request):
    if request.method == 'POST':
        account = request.user.account
        preferences, created = UserPreference.objects.get_or_create(account=account)
        for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
            setattr(preferences, field, request.POST.get(field))
        preferences.save()
        account.preferences = preferences
        account.save()
        
        product_list = FashionProduct.objects.all()
        filtered_products = filter_products_by_preferences(product_list, preferences)
        
        data = [{
            'id': product.id,
            'name': product.productDisplayName,
            'image_url': product.imageURL,
        } for product in filtered_products]

        return JsonResponse(data, safe=False)


@login_required(login_url='userlogin')
def updateLike(request):
    data = json.loads(request.body)
    product_info = data['productId']
    action = data['action']
    source = data.get('source', '')

    account = request.user.account

    if source == 'likes':
        match = re.search(r'(?<=\/images\\).+?(?=.jpg)', product_info)
        if match:
            product_id = int(match.group())
        else:
            product_id = int(product_info)
    else:
        product_id = int(product_info)

    product = FashionProduct.objects.get(id=product_id)

    likes, created = Likes.objects.get_or_create(account=account)
    orderItem, created = LikeItem.objects.get_or_create(likes=likes, product=product)

    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()
    elif action == 'superlike':
        orderItem.quantity += 1
        orderItem.superliked = not orderItem.superliked  
        orderItem.save()
    elif action == 'remove':
        orderItem.delete()

    response_data = {
        'message': f'Superliked {product_id}' if action == 'superlike' and orderItem.superliked else 'Item was added',
        'productId': product_id,
        'superliked': orderItem.superliked  
    }

    return JsonResponse(response_data, safe=False)
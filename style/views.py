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

# Define the style view, requiring user login
@login_required(login_url='userlogin')
def style(request):
    # Get account, likes, and liked items information for the logged-in user
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

    # Create a paginator object and get the current page of products
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

# Define the delete_product view, requiring staff member access
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

# Define the filter_products_by_preferences view
def filter_products_by_preferences(product_list, preferences):
    # Initialize the filtered products list with the input product list
    filtered_products = product_list

    # Iterate through the fields in the preferences object
    for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
        # Get the value of the field from the preferences object
        value = getattr(preferences, field, None)
        # If the field has a value, filter the products list by the field and its value
        if value:
            filtered_products = filtered_products.filter(**{field: value})
    
    # Set the number of products to show to 6
    num_products = 6
    # If the number of filtered products is greater than the desired number of products, return a random sample of the products
    if len(filtered_products) > num_products:
        return random.sample(list(filtered_products), num_products)
    # Otherwise, return the filtered products
    else:
        return filtered_products

# Define the survey view, requiring user login
@login_required(login_url='userlogin')
def survey(request):
    # If the request method is POST, update the user preferences and redirect to the style page
    if request.method == 'POST':
        # Get the account and preferences objects for the logged-in user
        account = request.user.account
        preferences, created = UserPreference.objects.get_or_create(account=account)

        # Save the previous gender preference
        prev_gender = preferences.gender

        # Iterate through the fields in the preferences object and update their values from the POST request
        for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
            setattr(preferences, field, request.POST.get(field))
        # Save the updated preferences object
        preferences.save()
        # Update the account's preferences field and save the account
        account.preferences = preferences
        account.save()

        # Update likes after saving preferences
        likes, _ = Likes.objects.get_or_create(account=account)

        # Redirect to the style page
        return redirect('style')

    # If the request method is not POST, display the survey page with filtered products based on the user's preferences
    product_list = FashionProduct.objects.all()
    user_preferences = request.user.account.preferences
    filtered_products = filter_products_by_preferences(product_list, user_preferences)

    context = {'filtered_products': filtered_products, 'user_preferences': user_preferences}
    return render(request, 'style/survey.html', context)

# Define the clear_preferences view, requiring user login
@login_required(login_url='userlogin')
def clear_preferences(request):
    # Get the account and preferences objects for the logged-in user
    account = request.user.account
    preferences, created = UserPreference.objects.get_or_create(account=account)

    # Clear the values of all fields in the preferences object
    preferences.gender = ''
    preferences.masterCategory = ''
    preferences.subCategory = ''
    preferences.articleType = ''
    preferences.baseColour = ''
    preferences.season = ''
    preferences.year = ''
    preferences.usage = ''

    # Save the updated preferences object and update the account's preferences field
    preferences.save()
    account.preferences = preferences
    account.save()
    return JsonResponse({'success': True})

# Define the delete_account view, requiring user login
@login_required
def delete_account(request):
    # If the request method is POST, delete the user account and associated data, and redirect to the login page
    if request.method == 'POST':
        # Get the user, account, likes, like items, and user preferences objects for the logged-in user
        user = request.user
        account = user.account
        likes = Likes.objects.filter(account=account)
        like_items = LikeItem.objects.filter(likes__in=likes)
        user_preferences = UserPreference.objects.filter(account=account)

        # Delete the user's like items, likes, user preferences, account, and user objects
        like_items.delete()
        likes.delete()
        user_preferences.delete()
        account.delete()
        user.delete()

        # Logout the user and redirect to the login page
        logout(request)

        # Add a success message to the request and redirect to the login page
        messages.success(request, 'User account successfully deleted.')
        return redirect('userlogin')
    # If the request method is not POST, display the account deletion confirmation page
    else:
        return render(request, 'style/delete_account_confirm.html')

# Define the likes view, requiring user login
@login_required(login_url='userlogin')
def likes(request):
    # Get the account and likes objects for the logged-in user
    account = request.user.account
    likes, created = Likes.objects.get_or_create(account=account)

    # Get the like items associated with the user's likes and the recommended images for each item
    items = likes.likeitem_set.all()
    likesItems = likes.get_likes_items
    filter_type = request.GET.get('filter', 'articleType')

    items_by_filter = {}
    recommended_images = {}
    product_image_urls = []

    start_time = time.time()

    # Iterate through the like items and group them by the selected filter type
    for item in items:
        items_by_filter.setdefault(getattr(item.product, filter_type), []).append(item)
        recommended_images[str(item.id)] = get_image_recommendations(item.product.id)
        product_image_urls.append(item.product.imageURL)

    # Get the user's gender preference and create weights for the product images based on whether they are superliked or not
    user_gender = account.preferences.gender if account.preferences and account.preferences.gender else None
    product_image_weights = [1.5 if item.superliked else 1 for item in items]

    # Get the mean likes recommendations for all product images and for each filter value based on the selected filter type
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

    end_time = time.time()

    # Print the execution time for the recommendations
    print(f"Execution time for entire recommendations: {end_time - start_time} seconds")

    # Add the necessary data to the context and render the likes page
    context = {
        'items_by_filter': items_by_filter,
        'filter_type': filter_type,
        'likes': likes,
        'likesItems': likesItems,
        'recommended_images': recommended_images,
        'filter_mean_recommendations': filter_mean_recommendations,
    }
    return render(request, 'style/likes.html', context)

# Define the remove_all_likes view, requiring user login
@login_required(login_url='userlogin')
def remove_all_likes(request):
    # Get the account and likes objects for the logged-in user
    account = request.user.account
    likes, created = Likes.objects.get_or_create(account=account)

    # Get the like items associated with the user's likes and delete them
    items = likes.likeitem_set.all()
    items.delete()

    # Add a success message to the request and redirect to the likes page
    messages.success(request, 'Likes cleared')
    return redirect('likes')

# Define the get_filtered_products view
def get_filtered_products(request):
    # If the request method is POST, update the user's preferences and return the filtered products as JSON
    if request.method == 'POST':
        # Get the account and preferences objects for the logged-in user and update the preferences
        account = request.user.account
        preferences, created = UserPreference.objects.get_or_create(account=account)
        for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
            setattr(preferences, field, request.POST.get(field))
        preferences.save()
        account.preferences = preferences
        account.save()

        # Get all the fashion products and filter them by the updated preferences
        product_list = FashionProduct.objects.all()
        filtered_products = filter_products_by_preferences(product_list, preferences)

        # Create a list of dictionaries representing the filtered products with their id, name, and image URL
        data = [{
            'id': product.id,
            'name': product.productDisplayName,
            'image_url': product.imageURL,
        } for product in filtered_products]

        # Return the filtered products as JSON
        return JsonResponse(data, safe=False)

# Define the updateLike view, requiring user login
@login_required(login_url='userlogin')
def updateLike(request):
    # Parse the JSON request body to get the product ID, action, and source
    data = json.loads(request.body)
    product_info = data['productId']
    action = data['action']
    source = data.get('source', '')

    # Get the account associated with the logged-in user
    account = request.user.account

    # If the source is likes, extract the product ID from the image URL
    if source == 'likes':
        match = re.search(r'(?<=\/images\\).+?(?=.jpg)', product_info)
        if match:
            product_id = int(match.group())
        else:
            product_id = int(product_info)
    else:
        product_id = int(product_info)

    # Get the FashionProduct object corresponding to the product ID
    product = FashionProduct.objects.get(id=product_id)

    # Get the Likes and LikeItem objects associated with the user's account and the product
    likes, created = Likes.objects.get_or_create(account=account)
    likeitem, created = LikeItem.objects.get_or_create(likes=likes, product=product)

    # Update the LikeItem object based on the action
    if action == 'add':
        likeitem.likestatus += 1
        likeitem.save()
    elif action == 'superlike':
        likeitem.likestatus += 1
        likeitem.superliked = not likeitem.superliked  
        likeitem.save()
    elif action == 'remove':
        likeitem.delete()

    # Create a JSON response with a message, product ID, and superliked status
    response_data = {
        'message': f'Superliked {product_id}' if action == 'superlike' and likeitem.superliked else 'item was added to likes',
        'productId': product_id,
        'superliked': likeitem.superliked  
    }

    # Return the JSON response
    return JsonResponse(response_data, safe=False)

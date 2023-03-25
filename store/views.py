from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .accounts import *
from .models import * 
import os
import re
from numpy.linalg import norm
from .recommendations import get_image_recommendations, get_recommended_products, get_mean_cart_recommendations
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='userlogin')
def store(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    product_list = ProductTest.objects.all()
    user_preferences = request.user.customer.preferences
    recommended_products = get_recommended_products(product_list, user_preferences)

    paginator = Paginator(recommended_products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

@login_required(login_url='userlogin')
def survey(request):
    if request.method == 'POST':
        customer = request.user.customer
        preferences, created = UserPreference.objects.get_or_create(customer=customer)
        for field in ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']:
            setattr(preferences, field, request.POST.get(field))
        preferences.save()
        customer.preferences = preferences
        customer.save()
        return redirect('store')

    return render(request, 'store/survey.html')

@login_required(login_url='userlogin')
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    items_by_master_category = {}
    recommended_images = {}
    product_image_urls = []

    for item in sorted(items, key=lambda item: item.product.masterCategory):
        items_by_master_category.setdefault(item.product.masterCategory, []).append(item)
        recommended_images[str(item.id)] = get_image_recommendations(item.product.id)
        product_image_urls.append(item.product.imageURL)

    mean_cart_recommendations = get_mean_cart_recommendations(product_image_urls)

    master_category_mean_recommendations = {
        master_category: get_mean_cart_recommendations([item.product.imageURL for item in master_category_items])
        for master_category, master_category_items in items_by_master_category.items()
    }

    context = {
        'items_by_master_category': items_by_master_category,
        'order': order,
        'cartItems': cartItems,
        'recommended_images': recommended_images,
        'master_category_mean_recommendations': master_category_mean_recommendations,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='userlogin')
def updateItem(request):
    data = json.loads(request.body)
    product_info = data['productId']
    action = data['action']
    source = data.get('source', '')

    customer = request.user.customer

    if source == 'cart':
        match = re.search(r'(?<=\/images\\).+?(?=.jpg)', product_info)
        if match:
            product_id = int(match.group())
        else:
            product_id = int(product_info)
    else:
        product_id = int(product_info)

    product = ProductTest.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()
    elif action == 'remove':
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

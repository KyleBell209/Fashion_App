import os
import re
from .models import *
import pickle
import cv2
import numpy as np
import tensorflow
from numpy.linalg import norm
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.preprocessing import image
import requests
from urllib.request import urlopen
import tempfile
from concurrent.futures import ThreadPoolExecutor

# Load the pre-trained ResNet50 model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Create a new model that takes the output of ResNet50 and applies global max pooling
model = tensorflow.keras.Sequential([
    base_model,
    GlobalMaxPooling2D()
])

# Load the pre-computed feature vectors and filenames
feature_list = np.array(pickle.load(open('embeddings.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

# Fit the NearestNeighbors object once and cache it
neighbors = NearestNeighbors(n_neighbors=11, algorithm='brute', metric='euclidean')
neighbors.fit(feature_list)

def process_image(image_source):
    if image_source.startswith('http'):  # If the image_source is a URL
        response = requests.get(image_source)
        temp_fd, temp_path = tempfile.mkstemp()
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(response.content)
        img = image.load_img(temp_path, target_size=(224, 224))
        os.close(temp_fd)
        os.remove(temp_path)
    else:  # If the image_source is a local path
        img = image.load_img(image_source, target_size=(224, 224))

    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    return preprocessed_img

def get_feature_vector(preprocessed_img):
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

def get_related_product_masterCategory(image_url):
    match = re.search(r'(?<=/images\\).+?(?=.jpg)', image_url)
    if match:
        product_id = int(match.group())
        related_product = ProductTest.objects.get(id=product_id)
        return related_product.masterCategory
    else:
        return None

def get_liked_product_ids(customer):
    likes, _ = Likes.objects.get_or_create(customer=customer, complete=False)
    like_items = likes.likeitem_set.all()
    like_item_product_ids = [item.product.id for item in like_items]
    return like_item_product_ids

def get_image_recommendations(product_id):
    existing_recommendations = RecommendedImage.objects.filter(product_id=product_id)

    if existing_recommendations.exists():
        return existing_recommendations


    product = ProductTest.objects.get(id=product_id)
    master_category = product.masterCategory
    product_gender = product.gender  # Fetch product gender
    image_url = product.imageURL
    preprocessed_img = process_image(image_url)
    normalized_result = get_feature_vector(preprocessed_img)

    distances, indices = neighbors.kneighbors([normalized_result])

    if product_gender:  # If product_gender is set, filter based on gender
        recommended_images = [
            RecommendedImage(
                product_id=product_id,
                masterCategory=master_category,
                related_product_masterCategory=get_related_product_masterCategory(
                    f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
                ),
                image_url=f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
            ) for file in indices[0][1:6] if ProductTest.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}').group())).gender == product_gender
        ]
    else:  # If product_gender is not set, do not filter based on gender
        recommended_images = [
            RecommendedImage(
                product_id=product_id,
                masterCategory=master_category,
                related_product_masterCategory=get_related_product_masterCategory(
                    f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
                ),
                image_url=f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
            ) for file in indices[0][1:6]
        ]

    recommended_images = [rec_image for rec_image in recommended_images if (not product_gender or rec_image.product.gender == product_gender)]

    RecommendedImage.objects.bulk_create(recommended_images)

    return recommended_images


def process_image_and_extract_features(image_source):
    preprocessed_img = process_image(image_source)
    return get_feature_vector(preprocessed_img)

def get_mean_likes_recommendations(product_image_urls, customer, master_category=None, gender=None, articleType=None, subCategory=None):
    if len(product_image_urls) == 0:
        return []

    like_item_product_ids = get_liked_product_ids(customer)

    with ThreadPoolExecutor() as executor:
        feature_vectors = list(executor.map(process_image_and_extract_features, product_image_urls))

    mean_feature_vector = np.mean(feature_vectors, axis=0)
    mean_feature_vector = np.nan_to_num(mean_feature_vector)
    mean_feature_vector = mean_feature_vector.reshape(1, -1)

    distances, indices = neighbors.kneighbors(mean_feature_vector)

    def get_product_name_from_url(image_url):
        match = re.search(r'(?<=/images\\).+?(?=.jpg)', image_url)
        if match:
            product_id = int(match.group())
            related_product = ProductTest.objects.get(id=product_id)
            return related_product.productDisplayName
        else:
            return "Product not found"

    recommended_images = [{'image_url': f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}',
                        'product_name': get_product_name_from_url(f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'),
                        'master_category': get_related_product_masterCategory(f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'),
                        'product_id': int(re.search(r'(?<=/images\\).+?(?=.jpg)', f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}').group())}
                        for file in indices[0][1:]]

    
    if master_category is not None:
            recommended_images = [rec_image for rec_image in recommended_images if rec_image['master_category'] == master_category]

    if gender is not None:
            recommended_images = [rec_image for rec_image in recommended_images if ProductTest.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).gender == gender]

    if articleType is not None:
            recommended_images = [rec_image for rec_image in recommended_images if ProductTest.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).articleType == articleType]

    if subCategory is not None:
            recommended_images = [rec_image for rec_image in recommended_images if ProductTest.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).subCategory == subCategory]

    recommended_images = [rec_image for rec_image in recommended_images if rec_image['product_id'] not in like_item_product_ids]

    return recommended_images


def get_recommended_products(product_list, user_preferences):
    if user_preferences is None:
        return product_list
    
    recommended_products = [
        product for product in product_list
        if (
            (not user_preferences.gender or user_preferences.gender == product.gender) and
            (not user_preferences.masterCategory or user_preferences.masterCategory == product.masterCategory) and
            (not user_preferences.subCategory or user_preferences.subCategory == product.subCategory) and
            (not user_preferences.articleType or user_preferences.articleType == product.articleType) and
            (not user_preferences.baseColour or user_preferences.baseColour == product.baseColour) and
            (not user_preferences.season or user_preferences.season == product.season) and
            (not user_preferences.year or user_preferences.year == product.year) and
            (not user_preferences.usage or user_preferences.usage == product.usage)
        )
    ]

    return recommended_products
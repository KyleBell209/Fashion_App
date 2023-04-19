import os
import re
from .models import *
import pickle
import cv2
import numpy as np
import tensorflow
from numpy.linalg import norm
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.applications.resnet import ResNet101, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.preprocessing import image
import requests
from urllib.request import urlopen
import tempfile
from concurrent.futures import ThreadPoolExecutor
import time
from functools import lru_cache

# Load the pre-trained model
base_model = ResNet101(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Create a new model that takes the output of the model and applies global max pooling
model = tensorflow.keras.Sequential([
    base_model,
    GlobalMaxPooling2D()
])

# Load the pre-computed feature vectors and filenames
feature_list = np.array(pickle.load(open('101embeddings.pkl', 'rb')))
filenames = pickle.load(open('101filenames.pkl', 'rb'))

# Fit the NearestNeighbors object once and cache it
neighbors = NearestNeighbors(n_neighbors=16, algorithm='brute', metric='cosine')
neighbors.fit(feature_list)

# Function to preprocess image and return preprocessed image
def process_image(image_source):
    if image_source.startswith('http'):  # If the image_source is a URL
        response = requests.get(image_source)  # Make a GET request to the URL
        temp_fd, temp_path = tempfile.mkstemp()  # Create a temporary file and get its file descriptor and path
        with open(temp_path, 'wb') as temp_file:  # Open the temporary file in write binary mode
            temp_file.write(response.content)  # Write the response content to the temporary file
        img = image.load_img(temp_path, target_size=(224, 224))  # Load the image from the temporary file
        os.close(temp_fd)  # Close the file descriptor
        os.remove(temp_path)  # Remove the temporary file from disk
    else:  # If the image_source is a local path
        img = image.load_img(image_source, target_size=(224, 224))

    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    return preprocessed_img

# Function to get the feature vector for the preprocessed image
def get_feature_vector(preprocessed_img):
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

# Function to get the related product's master category
def get_related_product_masterCategory(image_url):
    match = re.search(r'(?<=/images\\).+?(?=.jpg)', image_url)
    if match:
        product_id = int(match.group())
        related_product = FashionProduct.objects.get(id=product_id)
        return related_product.masterCategory
    else:
        return None

def get_image_recommendations(product_id):
    # Start time of function execution
    start_time = time.time()

    # Check if existing recommendations exist for this product_id
    existing_recommendations = RecommendedImage.objects.filter(product_id=product_id)

    if existing_recommendations.exists():
        # If existing recommendations exist, return them
        return existing_recommendations

    # Fetch product details for the given product_id
    product = FashionProduct.objects.get(id=product_id)
    master_category = product.masterCategory
    product_gender = product.gender
    image_url = product.imageURL

    # Preprocess the product image
    preprocessed_img = process_image(image_url)

    # Extract features from the preprocessed image
    normalized_result = get_feature_vector(preprocessed_img)

    # Find the nearest neighbors to the product image in the feature space
    distances, indices = neighbors.kneighbors([normalized_result])

    if product_gender:
        # If the product has a gender attribute set, filter the recommended images based on gender
        recommended_images = [
            RecommendedImage(
                product_id=product_id,
                masterCategory=master_category,
                related_product_masterCategory=get_related_product_masterCategory(
                    f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
                ),
                image_url=f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'
            ) for file in indices[0][1:6] if FashionProduct.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}').group())).gender == product_gender
        ]
    else:
        # If the product does not have a gender attribute set, do not filter the recommended images
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

    # Filter recommended images again based on product_gender
    recommended_images = [rec_image for rec_image in recommended_images if not product_gender or rec_image.product.gender == product_gender]

    # Bulk create recommended images in the database
    RecommendedImage.objects.bulk_create(recommended_images)

    # End time of function execution
    end_time = time.time()

    # Calculate and print the execution time
    print(f"Execution time for get_image_recommendations: {end_time - start_time} seconds")

    # Return the list of recommended images
    return recommended_images

# Function to process image and extract features with caching
@lru_cache(maxsize=256)  # Add caching decorator to cache the results of this function
def process_image_and_extract_features(image_source):
    preprocessed_img = process_image(image_source)
    return get_feature_vector(preprocessed_img)

# Function to get mean likes-based recommendations with various filtering options
def get_mean_likes_recommendations(product_image_urls, weights=None, master_category=None, gender=None, articleType=None, subCategory=None):
    # Start time of function execution
    start_time = time.time()

    # If product_image_urls is empty, return an empty list
    if len(product_image_urls) == 0:
        return []

    # If weights is not provided, initialize it to 1 for each product_image_url
    if weights is None:
        weights = [1] * len(product_image_urls)
    # If the length of weights does not match the length of product_image_urls, raise a ValueError
    elif len(weights) != len(product_image_urls):
        raise ValueError("Length of weights must match the length of product_image_urls")

    # Perform batch processing to reduce overhead
    batch_size = 32
    num_batches = int(np.ceil(len(product_image_urls) / batch_size))
    feature_vectors = []

    for i in range(num_batches):
        batch_image_urls = product_image_urls[i * batch_size : (i + 1) * batch_size]
        # Use ThreadPoolExecutor to parallelize feature extraction for each image in the batch
        with ThreadPoolExecutor() as executor:
            batch_feature_vectors = list(executor.map(process_image_and_extract_features, batch_image_urls))
        feature_vectors.extend(batch_feature_vectors)

    # Calculate the weighted mean of feature vectors
    mean_feature_vector = np.average(feature_vectors, axis=0, weights=weights)
    mean_feature_vector = np.nan_to_num(mean_feature_vector)
    mean_feature_vector = mean_feature_vector.reshape(1, -1)

    # Find the nearest neighbors to the mean feature vector in the feature space
    distances, indices = neighbors.kneighbors(mean_feature_vector)

    def get_product_name_from_url(image_url):
        # Extract the product ID from the image URL and fetch the corresponding FashionProduct object
        match = re.search(r'(?<=/images\\).+?(?=.jpg)', image_url)
        if match:
            product_id = int(match.group())
            related_product = FashionProduct.objects.get(id=product_id)
            return related_product.productDisplayName
        else:
            return "Product not found"

    # Generate a list of recommended images using the nearest neighbors
    recommended_images = [{'image_url': f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}',
                           'product_name': get_product_name_from_url(f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}'),
                           'master_category': get_related_product_masterCategory(f'https://storage.googleapis.com/django-bucket-kb/{filenames[file]}')}
                          for file in indices[0][1:]]
    # Filter recommended images based on the master_category, if provided
    if master_category is not None:
            recommended_images = [rec_image for rec_image in recommended_images if rec_image['master_category'] == master_category]

    # Filter recommended images based on the gender if provided
    if gender is not None:
            recommended_images = [rec_image for rec_image in recommended_images if FashionProduct.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).gender == gender]

    # Filter recommended images based on the articleType if provided
    if articleType is not None:
            recommended_images = [rec_image for rec_image in recommended_images if FashionProduct.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).articleType == articleType]

    # Filter recommended images based on the subCategory if provided
    if subCategory is not None:
            recommended_images = [rec_image for rec_image in recommended_images if FashionProduct.objects.get(id=int(re.search(r'(?<=/images\\).+?(?=.jpg)', rec_image['image_url']).group())).subCategory == subCategory]

    # End time of function execution
    end_time = time.time()

    # Calculate and print the execution time
    print(f"Execution time for mean recommendations: {end_time - start_time} seconds")

    # Return the list of recommended images
    return recommended_images

# Function to get recommended products based on user preferences
def get_recommended_products(product_list, user_preferences):
    # If user_preferences is None, return the original product list
    if user_preferences is None:
        return product_list
    
    # Generate a list of recommended products based on the user preferences
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

    # Return the list of recommended products
    return recommended_products

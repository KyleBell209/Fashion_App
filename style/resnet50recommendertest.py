import os
import re
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
import time

# Define the base directory for the image files
BASE_DIR = './static/'

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
neighbors = NearestNeighbors(n_neighbors=11, algorithm='brute', metric='cosine')
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

def get_image_recommendations(image_url):
    start_time = time.time()

    preprocessed_img = process_image(image_url)
    normalized_result = get_feature_vector(preprocessed_img)

    distances, indices = neighbors.kneighbors([normalized_result])

    recommended_images = [filenames[file].replace('\\', '/').replace('./static/', '') for file in indices[0][1:6]]

    end_time = time.time()

    print(f"Execution time for get_image_recommendations: {end_time - start_time} seconds")

    return recommended_images

def process_image_and_extract_features(image_source):
    preprocessed_img = process_image(image_source)
    return get_feature_vector(preprocessed_img)

input_image = './static/images/1163.jpg'
recommended_images = get_image_recommendations(input_image)

print("Recommended images:")
for idx, img_path in enumerate(recommended_images):
    print(f"{idx + 1}: {img_path}")
    adjusted_img_path = os.path.join(BASE_DIR, img_path)
    temp_img = cv2.imread(adjusted_img_path)
    if temp_img is not None:      
        cv2.waitKey(0)
    else:
        print(f"Could not load image {adjusted_img_path}. Please check the path.")
cv2.destroyAllWindows()

def average_precision(true_relevant, recommended):
    ap = 0
    relevant_count = 0

    for i, rec in enumerate(recommended):
        if rec in true_relevant:
            relevant_count += 1
            ap += relevant_count / (i + 1)

    if relevant_count == 0:
        return 0

    return ap / relevant_count

def mean_average_precision(ground_truth, recommendations):
    ap_sum = 0
    num_queries = len(ground_truth)

    for img_id, true_relevant in ground_truth.items():
        recommended = recommendations[img_id]
        ap_sum += average_precision(true_relevant, recommended)

    return ap_sum / num_queries

ground_truth = {
    '1163.jpg': ['images/13892.jpg', 'images/1164.jpg', 'images/13891.jpg', 'images/3042.jpg', 'images/3313.jpg'],
}

recommendations = {}

for img_id in ground_truth.keys():
    recommendations[img_id] = get_image_recommendations(os.path.join(BASE_DIR, f"images/{img_id}"))

def precision_recall_f1(true_relevant, recommended):
    tp = 0
    fp = 0
    fn = 0

    for rec in recommended:
        if rec in true_relevant:
            tp += 1
        else:
            fp += 1

    fn = len(true_relevant) - tp

    precision = tp / (tp + fp) if tp + fp != 0 else 0
    recall = tp / (tp + fn) if tp + fn != 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0

    return precision, recall, f1

def mean_precision_recall_f1(ground_truth, recommendations):
    precision_sum = 0
    recall_sum = 0
    f1_sum = 0
    num_queries = len(ground_truth)

    for img_id, true_relevant in ground_truth.items():
        recommended = recommendations[img_id]
        precision, recall, f1 = precision_recall_f1(true_relevant, recommended)

        precision_sum += precision
        recall_sum += recall
        f1_sum += f1

    mean_precision = precision_sum / num_queries
    mean_recall = recall_sum / num_queries
    mean_f1 = f1_sum / num_queries

    return mean_precision, mean_recall, mean_f1

mean_precision, mean_recall, mean_f1 = mean_precision_recall_f1(ground_truth, recommendations)
print(f"Mean Precision: {mean_precision}")
print(f"Mean Recall: {mean_recall}")
print(f"Mean F1 Score: {mean_f1}")

map_score = mean_average_precision(ground_truth, recommendations)
print(f"Mean Average Precision: {map_score}")


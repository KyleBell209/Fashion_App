# Load the necessary libraries
import pickle
import tensorflow
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
import cv2

# Load the model
feature_list = np.array(pickle.load(open('embeddings.pkl','rb')))
filenames = pickle.load(open('filenames.pkl','rb'))

model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

# Load the query image and preprocess it
img = image.load_img('sample/3313.jpg',target_size=(224,224))
img_array = image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocessed_img = preprocess_input(expanded_img_array)

# Compute the feature vector and normalize it
result = model.predict(preprocessed_img).flatten()
normalized_result = result / norm(result)

# Perform a nearest neighbor search
neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='cosine')
neighbors.fit(feature_list)

distances,indices = neighbors.kneighbors([normalized_result])

# Display the images side by side
images = []
for file in indices[0][1:6]:
    temp_img = cv2.imread(filenames[file])
    images.append(cv2.resize(temp_img,(512,512)))

cv2.imshow("output", np.hstack(images))
cv2.waitKey(0)
cv2.destroyAllWindows()

# Content-Based Fashion Recommender Django Application
This repository contains an image-based recommendation system that recommends similar images based on the input image. It uses a pre-trained ResNet101 model, feature extraction, Nearest Neighbors, and various filtering options to provide accurate recommendations. It also includes caching for efficient image processing.

## Features
* Pre-trained ResNet101 model for feature extraction.

* Nearest Neighbors for finding similar images.

* Various filtering options for refining recommendations based on gender, master category, article type, and subcategory.

* Caching for efficient image processing.
Parallelization of feature extraction using ThreadPoolExecutor.

* Mean likes-based recommendations with filtering options.

* Preferences dashboard giving the user the ability to filter the clothing products.

* Accounts can be created and deleted, the liked products are assigned to whatever account they were liked by.
## Cloning the application
Clone the repository using this command
```bash
git clone https://github.com/KyleBell209/Fashion_App.git
```

Install the requirements.txt
```bash
pip install -r requirements.txt
```

## Usage
How to run the application
```bash
python manage.py runserver
```

## Disclaimer
Beware that the initial time to generate recommendations may take a while, this is due to TensorFlow needing to be initialized.
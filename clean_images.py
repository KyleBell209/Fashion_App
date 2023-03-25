import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

# Import Django and models
import django
from store.models import ProductTest

django.setup()

# Define the target master categories
target_categories = [
    "Free Items", 
    "Home", 
    "Personal Care", 
    "Sporting Goods", 
    "Bath and Body", 
    "Beauty Accessories", 
    "Eyes", 
    "Fragrance", 
    "Free Gifts", 
    "Hair", 
    "Home Furnishing", 
    "Innerwear", 
    "Lips", 
    "Makeup", 
    "Mufflers", 
    "Perfumes", 
    "Nails", 
    "Skin", 
    "Skin Care", 
    "Sports Equipment", 
    "Umbrellas", 
    "Vouchers", 
    "Wallets", 
    "Water Bottles",
    "Baby Dolls",
    "Basketballs",
    "Bath Robe",
    "Beauty Accessory",
    "Body Lotion",
    "Body Wash and Scrub",
    "Concealer",
    "Cushion Covers",
    "Deodorant",
    "Eye Cream",
    "Eyeshadow",
    "Face Moisturisers",
    "Face Scrub and Exfoliator",
    "Face Serum and Gel",
    "Face Wash and Cleanser",
    "Footballs",
    "Foundation and Primer",
    "Fragrance Gift Set",
    "Hair Accessory",
    "Hair Colour",
    "Highlighter and Blush",
    "Ipad",
    "Kajal and Eyeliner",
    "Lehenga Choli",
    "Lip Care",
    "Lip Gloss",
    "Lip Liner",
    "Lip Plumper",
    "Lipstick",
    "Makeup Remover",
    "Mascara",
    "Mask and Peel",
    "Mens Grooming Kit",
    "Mufflers",
    "Nail Essentials",
    "Nail Polish",
    "Sunscreen",
    "Tights",
    "Water Bottle",
    "Toner",
    "Travel Accessory",
    "Umbrella",
    "Boys",
    "Girls",
]

# Retrieve the products with the specified category values
target_masterCategories = ProductTest.objects.filter(masterCategory__in=target_categories)
target_subCategories = ProductTest.objects.filter(subCategory__in=target_categories)
target_articleType = ProductTest.objects.filter(articleType__in=target_categories)
target_gender = ProductTest.objects.filter(gender__in=target_categories)

# Set file permissions for the static\images\ folder
folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), "static/images")
os.chmod(folder_path, 0o777) # Sets read, write, and execute permissions for all users

# Loop through the products and delete the associated images
for product in target_masterCategories:
    image_path = os.path.join(folder_path, product.imagePath)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    else:
        print(f"Image not found: {image_path}")

for product in target_subCategories:
    image_path = os.path.join(folder_path, product.imagePath)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    else:
        print(f"Image not found: {image_path}")

for product in target_articleType:
    image_path = os.path.join(folder_path, product.imagePath)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    else:
        print(f"Image not found: {image_path}")

for product in target_gender:
    image_path = os.path.join(folder_path, product.imagePath)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    else:
        print(f"Image not found: {image_path}")

# Loop through the products and delete the associated database entries
for product in target_masterCategories:
    product.delete()
    print(f"Deleted product with masterCategory: {product.masterCategory}")

for product in target_subCategories:
    product.delete()
    print(f"Deleted product with subCategory: {product.subCategory}")

for product in target_articleType:
    product.delete()
    print(f"Deleted product with articleType: {product.articleType}")

for product in target_gender:
    product.delete()
    print(f"Deleted product with articleType: {product.gender}")

# Reset file permissions for the static\images\ folder
os.chmod(folder_path, 0o755) # Sets read and execute permissions for all users

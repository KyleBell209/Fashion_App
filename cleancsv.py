import csv
import os

# Define target categories
target_categories = [
    "Free Items", 
    "Home", 
    "Socks",
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

# Define file paths
styles_file = "styles.csv"
output_file = "cleaned_styles.csv"

# Open input and output files
with open(styles_file, "r", newline='') as f_in, open(output_file, "w", newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    for row in reader:
        # Skip rows that contain target categories
        if any(category in row for category in target_categories):
            continue
        writer.writerow(row)

# Remove original styles.csv file and rename cleaned_styles.csv to styles.csv
os.remove(styles_file)
os.rename(output_file, styles_file)
import csv

def read_image_csv(csv_file_path):
    image_dict = {}
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_dict[row['filename']] = row['link']
    return image_dict

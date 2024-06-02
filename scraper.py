import csv
import json
import datetime

def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r', newline='', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, 'w', newline='', encoding='UTF-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Verileri CSV'den JSON'a dönüştür
csv_file_path = 'AmazonWebScraperDataset.csv'
json_file_path = 'static/data.json'
csv_to_json(csv_file_path, json_file_path)

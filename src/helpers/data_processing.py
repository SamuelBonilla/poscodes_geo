from src.config import *
import io
import pandas as pd
import requests
import pymongo
from pymongo import MongoClient


def request_geo_data(geo, collection):
    geo = dict(geo)
    response = requests.post('https://api.postcodes.io/postcodes', json=geo)
    if response.status_code == 200:
        for res in response.json()['result']:
            geo_data = res['result']
            if geo_data and len(geo_data):
                try:
                    collection.insert_many(geo_data)
                except Exception as e:
                    print(e)
                    pass


def load_data(url):
    client = MongoClient(
        'mongo', 
        27017,
        username=os.getenv('MONGO_ROOT_USER'),
        password=os.getenv('MONGO_ROOT_PASSWORD')
    )
    db = client.mi_aguila
    collection = db['mi-aguila']
    collection.create_index([('postcode', pymongo.ASCENDING)],
        unique=True
    )
    get_file = pyminio_client.get(url)
    df = pd.read_csv(io.BytesIO(get_file.data))
    df = df.drop_duplicates() # Delete duplicate data
    data = {
        "geolocations": []
    }
    for _, row in df.iterrows():
        if len(data['geolocations']) == 10:
            request_geo_data(data, collection)
            data['geolocations'] = []
            break
        else:
            data['geolocations'].append({
                "longitude": row['lon'],
                "latitude": row['lat']
            })
    return url
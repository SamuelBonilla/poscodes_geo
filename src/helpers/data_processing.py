from src.config import *
import io
import pandas as pd
import requests


def request_geo_data(geo):
    response = requests.post('https://api.postcodes.io/postcodes', json=geo)
    if response.status_code == 200:
        for res in response.json()['result']:
            geo_data = res['result']


def insert_in_db(data):
    pass


def load_data(url):
    get_file = pyminio_client.get(url)
    df = pd.read_csv(io.BytesIO(get_file.data))
    df = df.drop_duplicates() # Delete duplicate data
    data = {
        "geolocations": []
    }
    for _, row in df.iterrows():
        if len(data['geolocations']) == 10:
            request_geo_data(data)
            data['geolocations'] = []
            break
        else:
            data['geolocations'].append({
                "longitude": row['lon'],
                "latitude": row['lat']
            })
    return url
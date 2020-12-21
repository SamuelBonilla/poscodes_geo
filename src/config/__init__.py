from dotenv import load_dotenv
from pyminio import Pyminio
import os

load_dotenv()

pyminio_client = Pyminio.from_credentials(
    endpoint='minio:9000',
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)
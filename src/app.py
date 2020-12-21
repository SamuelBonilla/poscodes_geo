from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from src.config import *
from src.helpers.data_processing import load_data
import os
import redis
from rq import Queue


app = Flask(__name__)
redis_url = os.getenv('REDIS_URL')
conn = redis.from_url(redis_url)
q = Queue('data', connection=conn)



@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            bucket_name = f'/{os.getenv("MINIO_BUKET_NAME")}/'
            pyminio_client.mkdirs(f'{bucket_name}')
            size = os.fstat(uploaded_file.fileno()).st_size
            metadata = {
                'size': size,
                'content-type': uploaded_file.content_type
            }

            minio_file_name = f'{bucket_name}{secure_filename(uploaded_file.filename)}'
            pyminio_client.put_data(
                minio_file_name, 
                uploaded_file.read(), 
                metadata
            )

            q.enqueue(load_data, minio_file_name, timeout=23421342343)


            return f"""
                    object stored in bucket : http://localhost:9000{bucket_name}

                    We are processing your file in background :)
                """

    return render_template('form.html')
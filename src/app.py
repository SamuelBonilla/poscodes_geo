from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from src.config import *
import os

app = Flask(__name__)



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

            minio_file_name = f'{bucket_name}/{secure_filename(uploaded_file.filename)}'
            pyminio_client.put_data(
                minio_file_name, 
                uploaded_file.read(), 
                metadata
            )

            return f"""
                    object stored in bucket : http://localhost:9000{bucket_name}

                    We are processing your file in background :)
                """

    return render_template('form.html')
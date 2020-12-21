from flask import Flask, request, render_template
from pyminio import Pyminio
from werkzeug.utils import secure_filename
import src.config
import os

app = Flask(__name__)

pyminio_client = Pyminio.from_credentials(
    endpoint='minio:9000',
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False,
    publicUrl="0.0.0.0"
)


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
                    object stored in bucket : http://localhost:9000{minio_file_name}

                    We are processing your file in background :)
                """

    return render_template('form.html')
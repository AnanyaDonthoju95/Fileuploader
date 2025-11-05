# backend/app.py
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import boto3
import os
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Read AWS credentials from environment
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_BYTES", 5 * 1024 * 1024))

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Allowed extensions for upload
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.txt', '.pdf')

def allowed_file(filename):
    """Check if file has allowed extension"""
    return filename and filename.lower().endswith(ALLOWED_EXTENSIONS)

@app.route("/")
def home():
    return "✅ Flask AWS S3 File Uploader API is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No filename provided"}), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Validate file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({"error": "File too large (max 5MB)"}), 400

    # Generate unique filename
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3_key = f"{timestamp}_{filename}"

    try:
        # Upload to S3
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.content_type or "application/octet-stream"
            }
        )

        # Public file URL
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

        return jsonify({
            "message": "Upload successful",
            "url": file_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

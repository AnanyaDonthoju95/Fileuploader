# File Uploader

A web application that allows users to upload files (images, PDFs, text, etc.) to **AWS S3** and instantly receive a **direct download link**. The app demonstrates cloud storage integration, Python backend, and serverless deployment.

---

## Objective

- Enable users to upload files securely to AWS S3.
- Return a public S3 link after upload.
- Deploy frontend and backend on serverless-friendly platforms.

---

## Setup Instructions

1. **Backend (Python Flask)**
   - Install dependencies:
     ```bash
     pip install flask boto3 python-dotenv
     ```
   - Create a `.env` file with AWS credentials:
     ```
     AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
     AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
     AWS_REGION=YOUR_REGION
     S3_BUCKET_NAME=YOUR_BUCKET_NAME
     ```
   - Start the server locally (optional for testing):
     ```bash
     python app.py
     ```
   - Backend is deployed on **Render** at:  
     ```
     https://fileuploader-bvid.onrender.com
     ```

2. **Frontend (HTML/JS)**
   - Edit `script.js` to use your backend URL:
     ```javascript
     const CONFIG = {
         FLASK_API_URL: 'https://fileuploader-bvid.onrender.com'
     };
     ```
   - Open `index.html` in a browser for testing.
   - Frontend is deployed on **Vercel**.

3. **AWS S3 Storage**
   - Bucket configured with CORS to allow uploads from your frontend.
   - IAM user with `s3:PutObject` and `s3:GetObject` permissions.
   - Uploaded files are accessible via public S3 URLs.

---

## Features

- **File Upload:** Drag-and-drop or select files for upload.
- **Real-Time Progress:** Shows upload progress in a progress bar.
- **Direct Download Link:** Displays clickable S3 link after upload.
- **Responsive Design:** Works on both desktop and mobile.
- **Serverless Deployment:** Frontend on Vercel, backend on Render.

---

## How It Works

1. User selects a file on the frontend.
2. `XMLHttpRequest` sends the file to the Flask backend.
3. Backend uploads the file to AWS S3.
4. Backend returns the public S3 URL in JSON.
5. Frontend displays the link for the user to download or share.

---

## Challenges / Assumptions

- **CORS Handling:** Ensuring the frontend could communicate with the backend on Render required proper CORS configuration both in Flask and S3 bucket.  
- **AWS Security:** Keeping AWS credentials secure while allowing file uploads was critical. Used `.env` to avoid exposing keys.  
- **Public Access vs. Pre-Signed URLs:** For simplicity, uploaded files are publicly accessible via S3 URLs. In production, pre-signed URLs would be more secure.  
- **File Validation:** Only basic file types (images, PDFs, text) are supported. Handling all possible file types and sizes would require additional validation.  
- **Serverless Deployment:** Ensuring smooth communication between Vercel (frontend) and Render (backend) while maintaining upload progress and error handling.  
- **Network Reliability:** Handling large file uploads reliably and showing accurate progress was a challenge with potential network interruptions.


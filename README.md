# 👤 Face Recognition Flask App

A computer-vision powered **Flask web application** that performs **face detection and recognition**
using a pre-trained PCA + SVM model, now enhanced with a **REST API for inference** and a
**Dockerized deployment setup**.

---

## 🚀 Features

- 🎯 **Face Detection** using OpenCV's Haar Cascade classifier  
- 🧠 **Face / Gender Recognition** using PCA (Eigenfaces) + SVM  
- 🌐 **Web UI** built with Flask templates for uploading and visualizing predictions  
- 🔌 **REST API** endpoint for programmatic inference (`/api/predict`)  
- 🐳 **Dockerized** with a production-ready `gunicorn` server  
- 📂 Clean project structure with separate modules for:
  - model artifacts (`model/`)
  - core logic (`app/`)
  - static assets (`static/`)
  - templates (`templates/`)

---

## 🏗️ Project Structure

```bash
4_Flask_App/
├── main.py               # Flask app entrypoint
├── app/
│   ├── face_recognition.py   # Core face recognition pipeline
│   └── views.py              # Flask views & REST API endpoint
├── model/
│   ├── haarcascade_frontalface_default.xml
│   ├── model_svm.pickle
│   └── pca_dict.pickle
├── static/
│   ├── images/               # Static images
│   └── predict/              # Generated prediction images
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── app.html
│   └── gender.html
├── test_images/              # Sample test images
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ Running Locally (Without Docker)

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Flask development server

```bash
python main.py
```

The app will be available at:

- Web UI: http://127.0.0.1:5000/
- Gender recognition form: http://127.0.0.1:5000/app/gender/

---

## 🔌 REST API: `/api/predict`

A new REST endpoint has been added for programmatic inference.

### Endpoint

- **URL:** `/api/predict`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Field:** `image` (or `image_name`)

### Example `curl` Request

```bash
curl -X POST http://127.0.0.1:5000/api/predict          -F "image=@test_images/01.jpg"
```

### Sample JSON Response

```json
{
  "num_faces": 1,
  "predictions": [
    {
      "prediction_name": "male",
      "score": 98.75
    }
  ]
}
```

- `num_faces` – number of detected faces in the image  
- `prediction_name` – predicted label (e.g., identity or gender)  
- `score` – prediction confidence (0–100%, depending on model output)

---

## 🐳 Docker Deployment

This project includes a `Dockerfile` for containerized deployment using **gunicorn**.

### 1️⃣ Build the image

```bash
docker build -t face-recognition-app .
```

### 2️⃣ Run the container

```bash
docker run -p 5000:5000 face-recognition-app
````

### 3️⃣ Access the app

- Web UI: http://localhost:5000/  
- REST API: http://localhost:5000/api/predict

---

## 🧠 How It Works (High-Level)

1. An uploaded image is read and converted to grayscale.  
2. Faces are detected using OpenCV's Haar Cascade classifier.  
3. Each face is projected into PCA (Eigenface) space.  
4. A trained SVM model classifies the face (e.g., identity or gender).  
5. The app returns:
   - Annotated image in the web UI (bounding boxes & labels)
   - JSON predictions via the REST API

---

## 🧑‍💻 Tech Stack

- **Backend:** Flask  
- **ML / CV:** OpenCV, scikit-learn, PCA, SVM  
- **Serving:** gunicorn  
- **Deployment:** Docker  

---

## 📌 Notes

- The actual model files (`model_svm.pickle`, `pca_dict.pickle`) and cascade XML
  are already referenced in `face_recognition.py`.  
- Ensure these paths remain valid if you change the project structure.

---

Enjoy hacking on face recognition 🔍👤

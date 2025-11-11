import os
import cv2
import numpy as np
from app.face_recognition import faceRecognitionPipeline
from flask import render_template, request, jsonify
import matplotlib.image as matimg


UPLOAD_FOLDER = 'static/upload'

def index():
    return render_template('index.html')


def app():
    return render_template('app.html')


def genderapp():
    if request.method == 'POST':
        f = request.files['image_name']
        filename = f.filename
        # save our image in upload folder
        path = os.path.join(UPLOAD_FOLDER,filename)
        f.save(path) # save image into upload folder
        # get predictions
        pred_image, predictions = faceRecognitionPipeline(path)
        pred_filename = 'prediction_image.jpg'
        cv2.imwrite(f'./static/predict/{pred_filename}',pred_image)
        
        # generate report
        report = []
        for i , obj in enumerate(predictions):
            gray_image = obj['roi'] # grayscale image (array)
            eigen_image = obj['eig_img'].reshape(100,100) # eigen image (array)
            gender_name = obj['prediction_name'] # name 
            score = round(obj['score']*100,2) # probability score
            
            # save grayscale and eigne in predict folder
            gray_image_name = f'roi_{i}.jpg'
            eig_image_name = f'eigen_{i}.jpg'
            matimg.imsave(f'./static/predict/{gray_image_name}',gray_image,cmap='gray')
            matimg.imsave(f'./static/predict/{eig_image_name}',eigen_image,cmap='gray')
            
            # save report 
            report.append([gray_image_name,
                           eig_image_name,
                           gender_name,
                           score])
            
        
        return render_template('gender.html',fileupload=True,report=report) # POST REQUEST
            
    
    
    return render_template('gender.html',fileupload=False) # GET REQUEST

def api_predict():
    """REST API endpoint: accepts an image file and returns predictions as JSON."""
    if 'image' not in request.files and 'image_name' not in request.files:
        return jsonify({'error': 'No image file provided. Use form field "image".'}), 400

    f = request.files.get('image') or request.files.get('image_name')
    if f.filename == '':
        return jsonify({'error': 'Empty filename.'}), 400

    # Read image bytes into OpenCV format
    file_bytes = np.frombuffer(f.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': 'Invalid image file.'}), 400

    # Run through recognition pipeline without saving to disk
    _, predictions = faceRecognitionPipeline(img, path=False)

    results = []
    for obj in predictions:
        results.append({
            'prediction_name': obj.get('prediction_name'),
            'score': float(obj.get('score', 0.0))
        })

    return jsonify({
        'num_faces': len(results),
        'predictions': results
    })

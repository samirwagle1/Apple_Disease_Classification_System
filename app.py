import cv2
import numpy as np
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
import joblib
from waitress import serve

app = Flask(__name__)

# Loading the trained model and encoded labels
loaded_model = joblib.load('trained_model.pkl')

label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('label_encoder_classes.npy')

# Function to extract color histogram features for new test image
def extract_color_histogram(image, bins=(8, 8, 8)):
    # Converting image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculating the color histogram
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    
    # Normalizing the histogram
    cv2.normalize(hist, hist)
    
    # Flattening the histogram into  a  2D feature vector
    hist = hist.flatten()
    
    return hist

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    try:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_img = cv2.resize(img, (250, 250))
        color_hist = extract_color_histogram(resized_img)
        prediction = loaded_model.predict([color_hist])[0]
        disease_type = label_encoder.inverse_transform([prediction])[0]
        
        # Render the result template with the classification
        if disease_type == 'SCAB':
            return render_template('scab.html', classification=disease_type)
        elif disease_type == 'BLOTCH':
            return render_template('blotch.html', classification=disease_type)
        elif disease_type == 'ROT':
            return render_template('rot.html', classification=disease_type)
        elif disease_type == 'NORMAL':
            return render_template('normal.html', classification=disease_type)
        else:
            return render_template('invalid.html', classification=disease_type)
    
    except Exception as e:
        return f"Error processing image: {e}" 

if __name__ == '__main__':
     serve(app, host="127.0.0.1", port=5000)
    
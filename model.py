import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Function to load and preprocess images from a folder
def load_and_preprocess_images(folder, target_size=(250, 250)):
    images = []
    labels = []
    
    # Iterating through each subfolder with disease name
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        
        # Checking if the item in the folder is a directory/sub-folder
        if os.path.isdir(subfolder_path):
            # Iterate through each image file in the subfolder
            for filename in os.listdir(subfolder_path):
                img_path = os.path.join(subfolder_path, filename)
                
                try:
                    # Reading the image with cv2
                    img = cv2.imread(img_path)
                    
                    # Checking if the image is loaded successfully
                    if img is None:
                        print(f"Error: Unable to read image '{img_path}'")
                        continue
                    
                    # Resizing image to a common size
                    resized_img = cv2.resize(img, target_size)
                    
                    images.append(resized_img)
                    labels.append(subfolder)
                
                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")
    
    return np.array(images), np.array(labels)

# Function to extract color histogram features
def extract_color_histogram(image, bins=(8, 8, 8)):
    # Converting image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculating the color histogram
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    
    # Normalizing the histogram
    cv2.normalize(hist, hist)
    
    # Flattening the histogram into a 1D feature vector
    hist = hist.flatten()
    
    return hist

# Specifying the dataset folder and preprocessing images
data_folder = './Dataset'
X, y = load_and_preprocess_images(data_folder)

# Encoding labels as the Disease Name
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
class_names = label_encoder.classes_

# Extracting features of the image using histrogram
X_features = []
for image in X:
    color_hist = extract_color_histogram(image)
    X_features.append(color_hist)

X_features = np.array(X_features)

# Spliting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_features, y_encoded, test_size=0.2, random_state=42)

# Training KNN (K-Nearest Neighbors) model
knnModel = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
knnModel.fit(X_train, y_train)

# Saving the Trained Model
joblib.dump(knnModel, 'trained_model.pkl')
np.save('label_encoder_classes.npy', label_encoder.classes_)

# Evaluating model
y_pred = knnModel.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
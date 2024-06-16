# pip install Flask tensorflow pillow
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

from PIL import Image

print("tensorflow version: ", tf.keras.__version__)

model = load_model("./skin_disease_weights/skindect_model.h5")

# {'1. Enfeksiyonel': 0,
#  '2. Ekzama': 1,
#  '3. Akne': 2,
#  '4. Pigment': 3,
#  '5. Benign': 4,
#  '6. Malign': 5}1

class_names = ['Infectious', 'Eczema', 'Acne', 'Pigment', 'Benign', 'Malignant']
class_names_persian = ['عفونی', 'اگزما', 'جوش‌های چربی (آکنه)', 'رنگدانه', 'خوش‌خیم', 'بدخیم']

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return jsonify({ "message": "ok"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        img = Image.open(file)
        img = img.resize((299, 299))  # Resize image to match model's expected input size
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        
        # Make prediction
        predictions = model.predict(img)
        print(predictions)
        predicted_class = np.argmax(predictions, axis=1)[0]
        print("p class", predicted_class)
        predicted_label = class_names[predicted_class]
        predicted_label_P = class_names_persian[predicted_class]
        confidence = float(predictions[0][predicted_class])
        print(confidence)
        if confidence < 0.40:
            return jsonify({'message': "پوست سالم است"})
        return jsonify({"predicted_class": predicted_label, "predicted_class_persian": predicted_label_P, "confidence": confidence})
    
    return jsonify({"error": "Unknown error"}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8585)

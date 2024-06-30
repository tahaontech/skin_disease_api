# pip install Flask tensorflow pillow
import os
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model

from PIL import Image
import chromadb


print("tensorflow version: ", tf.keras.__version__)

model = load_model("./skin_disease_weights/skindect_model.h5")

embedding_model = Model(inputs=model.input,
                                 outputs=model.get_layer("dense").output)



client = chromadb.PersistentClient(path="./chroma")
collection = client.get_collection(name="diseases")

def embedding_fn(img):
    img = img.resize((299, 299))  # Resize image to match model's expected input size
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
        
    # Make prediction
    predictions = embedding_model.predict(img)
    return predictions[0].tolist()


translated_list = {
    'Acne': 'آکنه',
    'Actinic_Keratosis': 'کراتوز اکتینیک',
    'Atopic_Dermatitis(Eczema)': 'درماتیت آتوپیک (اگزما)',
    'Basal_Cell_Carcinoma': 'کارسینوم سلول پایه',
    'Blisters': 'تاول',
    'Cellulitis': 'سلولیت',
    'Chickenpox': 'آبله مرغان',
    'Cold_Sores(Herpes Simplex)': 'زخم سرد (هرپس سیمپلکس)',
    'Contact_Dermatitis': 'درماتیت تماسی',
    'Cutaneous_Candidiasis': 'کاندیدیاز پوستی',
    'Dermatofibroma': 'درماتوفیبروم',
    'Drug_Rashes': 'راش‌های دارویی',
    'Erythema_Multiforme': 'اریتم مولتی‌فرم',
    'Folliculitis': 'فولیکولیت',
    'Herpes_Zoster(Shingles)': 'هرپس زوستر (زونا)',
    'Hives(Urticaria)': 'کهیر (اورتیکاریا)',
    'Impetigo': 'ایمپی تیگو',
    'Kaposis_Sarcoma': 'سارکوم کاپوزی',
    'Keloids': 'کلوئید',
    'Lichen_Planus': 'لیکن پلان',
    'Lupos': 'لوپوس',
    'Measles': 'سرخک',
    'Melanoma': 'ملانوما',
    'Moles(Nevi)': 'خال‌ها (نووس)',
    'Pityriasis_Rosea': 'پیتریازیس رزا',
    'Psoriasis': 'پسوریازیس',
    'Ringworm(Tinea)': 'قارچ پوستی (تینیا)',
    'Rosacea': 'روزاسه',
    'Scabies': 'جرب',
    'Seborrheic_Dermatitis': 'درماتیت سبورئیک',
    'Seborrheic_Keratosis': 'کراتوز سبورئیک',
    'Squamous_Cell_Carcinoma': 'کارسینوم سلول سنگفرشی',
    'Sunburn': 'آفتاب‌سوختگی',
    'Tinea_Versicolor': 'تینیا ورسیکالر',
    'Vitiligo': 'ویتیلیگو',
    'Warts(Human Papillomavirus)': 'زگیل (ویروس پاپیلومای انسانی)'
}

num_results = 5

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return jsonify({ "message": "ok", "classes": translated_list}), 200


@app.route('/predict_v2', methods=['POST'])
def predict_v2():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        img = Image.open(file)
        embedding = embedding_fn(img)  # Add batch dimension
        
        res = collection.query(
            query_embeddings=[embedding],
            n_results=num_results,
        )

        cls = [res["metadatas"][0][i]["class"] for i in range(num_results)]
        distanses = [res["distances"][0][i] for i in range(num_results)]

        return jsonify({"predicted_class": cls, "predicted_class_persian": [translated_list[cl] for cl in cls], "distances": distanses})
    
    return jsonify({"error": "Unknown error"}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8585)

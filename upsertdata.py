import os

from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model

from PIL import Image

import chromadb

client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="diseases")

model = load_model("./skin_disease_weights/skindect_model.h5")

embedding_model = Model(inputs=model.input,
                                 outputs=model.get_layer("dense").output)

def embedding_fn(img_path):
    img = Image.open(img_path)
    img = img.resize((299, 299))  # Resize image to match model's expected input size
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
        
    # Make prediction
    predictions = embedding_model.predict(img)
    return predictions[0].tolist()

data = []

for c in os.listdir("data"):
    print(c)
    for i, img in enumerate(os.listdir(os.path.join("data", c))):
        try:
            img_path =  os.path.join("data", c, img)
            # get embedding
            embedding = embedding_fn(img_path)
            data.append({
                "id": f"{c}-{i}",
                "class": c,
                "embedding": embedding,
                "img": img_path,
            })
        except:
            print(f"error on {c} and {img}")
            continue

# print(data)


collection.add(
    embeddings=[x["embedding"] for x in data],
    metadatas=[{"class": x["class"], "img": x["img"]} for x in data],
    ids=[x["id"] for x in data]
)

print(f"'{len(data)}' data is added to db")
# pip install Flask tensorflow pillow
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

from PIL import Image

img_shape = (299, 299, 3)
# addModel = tf.keras.applications.xception.Xception(input_shape=img_shape,
#                                            include_top=False,
#                                            weights='imagenet')

# model = Sequential()
# model.add(addModel)
# model.add(GlobalAveragePooling2D())
# model.add(Flatten())
# model.add(Dense(1024, activation="relu"))
# model.add(Dense(512, activation="relu"))
# model.add(Dense(6, activation="softmax" , name="classification"))
# model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.0007,momentum=0.9), 
#             loss='categorical_crossentropy',
#             metrics = ['accuracy'])


# model.load_weights("./skin_disease_weights/skindect_model_weights.h5")

print(tf.keras.__version__)

model = load_model("./skin_disease_weights/skindect_model.h5")

# {'1. Enfeksiyonel': 0,
#  '2. Ekzama': 1,
#  '3. Akne': 2,
#  '4. Pigment': 3,
#  '5. Benign': 4,
#  '6. Malign': 5}

class_names = ['enfeksyonel', 'Ekzema', 'Acne', 'Pigment', 'Benign', 'Malign']
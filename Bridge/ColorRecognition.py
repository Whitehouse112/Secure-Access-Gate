from keras.models import load_model
import numpy as np
import cv2
import os

def load(path_file):
    return load_model(path_file)

def color_recognition(img, model):
   
    img = cv2.resize(img, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
    img = np.expand_dims(img, axis=0)

    activations = model.predict(img)
    d_b = {0: 'black', 1:'blue', 2:'cyan', 3:'gray', 4:'green', 5:'red', 6:'white', 7:'yellow'}
    print("color:", d_b[np.argmax(activations)])

    return d_b[np.argmax(activations)]
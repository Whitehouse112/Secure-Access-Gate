from keras.models import load_model

import numpy as np
import cv2


model = load_model('vehicle_color_haze_free_model.h5')

img = cv2.imread("testFede1.jpg")

img = cv2.resize(img, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)

img = np.expand_dims(img, axis=0)

activations = model.predict(img)
d_b = {0: 'black', 1:'blue', 2:'cyan', 3:'gray', 4:'green', 5:'red', 6:'white', 7:'yellow'}
print("class:", d_b[np.argmax(activations)])
print(activations)
img = np.squeeze(img, axis=None)

cv2.imshow("img", img)
cv2.waitKey(0)
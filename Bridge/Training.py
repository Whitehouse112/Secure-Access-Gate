import numpy as np
import os
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from skimage.io import imread
from skimage.filters import threshold_otsu

dir_path = os.path.dirname(os.path.realpath(__file__))

# I caratteri I, O, Q, U non vengono utilizzati nelle targhe italiane
chars = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
            'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
        ]


def read_training_dataset(directory):
    images = []
    characters = []

    for char in chars:
        for each in range(10):
            img_path = os.path.join(directory, char, char + '_' + str(each) + '.jpg')
            gray = imread(img_path, as_gray=True)
            # Ottengo l'immagine binarizzata (solo bianco e nero) con Otsu.
            binary = gray < threshold_otsu(gray)
            # trasformo l'immagine in un vettore monodimensionale 1x400
            flattened = binary.reshape(-1)
            images.append(flattened)
            characters.append(char)

    return np.array(images), np.array(characters)


def cross_validation(model, folds, train_data, train_label):
    # Accuracy tramite cross validation
    accuracy = cross_val_score(model, train_data, train_label, cv=folds)
    print("Accuracy % using ", str(folds), "-fold")
    print(accuracy * 100)


print('Reading traning dataset...')
training_dataset_directory = f"{dir_path}\\train"
images, characters = read_training_dataset(training_dataset_directory)
print('Reading completed.')

# Il modello usato si chiama SVC (Support Vector Classification). Si è scelto questo perchè quando le immagini sono
# "poche" (320 nel nostro caso), il tempo impiegato non è alto.
svc_model = SVC(kernel='linear', probability=True)

cross_validation(svc_model, 4, images, characters)

print('Training...')
svc_model.fit(images, characters)
print("Training completed.")

print("Saving model...")
filename = './model.sav'
pickle.dump(svc_model, open(filename, 'wb'))
print("Model saved")

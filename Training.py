import numpy as np
# Per accedere a cartelle
import os
# Per salvare il modello
import pickle
# Per usare il modello
from sklearn.svm import SVC
# Per usare la cross validation
from sklearn.model_selection import cross_val_score
# Per leggere le immagini
from skimage.io import imread
# Per l'otsu thresholding
from skimage.filters import threshold_otsu

# I caratteri I, O, Q, U non ci sono perchè non vengono utilizzati nelle targhe italiane
chars = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
            'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
        ]


def read_training_dataset(directory):
    images = []
    characters = []
    # Per ogni carattere scorro ciascuna delle dieci immagini cha ogni carattere ha nel dataset di training, che sono
    # salvate come carattere_numeroImmagine
    for char in chars:
        for each in range(10):
            # Salvo il percorso dell'immagine corrente
            img_path = os.path.join(directory, char, char + '_' + str(each) + '.jpg')
            # Leggo l'immagine e la converto in scala di grigio
            gray = imread(img_path, as_gray=True)
            # Ottengo l'immagine binarizzata (solo bianco e nero) con Otsu.
            binary = gray < threshold_otsu(gray)
            # Il classificatore richiede che l'immagine di input sia monodimensionale, quindi trasformo l'immagine
            # dall'essere un vettore bidimensionale 20x20 all'essere un vettore monodimensionale 1x400
            flattened = binary.reshape(-1)
            images.append(flattened)
            characters.append(char)

    return np.array(images), np.array(characters)


def cross_validation(model, folds, train_data, train_label):
    # Misurare l'accuracy di un modello con la cross validation significa, dato un numero di piegamenti
    # (in questo caso 4), dividere il dataset in 4 parti e usarne tre per il training e una per il testing
    accuracy = cross_val_score(model, train_data, train_label, cv=folds)
    print("Accuracy % using ", str(folds), "-fold")
    print(accuracy * 100)


print('Reading traning dataset...')
training_dataset_directory = './train'
images, characters = read_training_dataset(training_dataset_directory)
print('Reading completed.')

# Il modello usato si chiama SVC (Support Vector Classification). Si è scelto questo perchè quando le immagini sono
# "poche" (320 nel nostro caso), il tempo impiegato non è alto.
# Se si vuole sapere quanto il modello sia certo della predizione che fa, bisogna settare probability a True
svc_model = SVC(kernel='linear', probability=True)

cross_validation(svc_model, 4, images, characters)

print('Training...')
svc_model.fit(images, characters)
print("Training completed.")

print("Saving model...")
filename = './model.sav'
pickle.dump(svc_model, open(filename, 'wb'))
print("Model saved")

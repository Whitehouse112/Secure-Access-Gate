import Segmentation
import pickle

def setup():
    print("Loading model...")
    filename = './files/model.sav'
    model = pickle.load(open(filename, 'rb'))
    print('Model loaded')
    return model

def prediction(model, chars, x_chars):

    classifications = []
    plate = ''
    ordered_plate = ''

    for character in chars:
        character = character.reshape(1, -1)
        result = model.predict(character)
        classifications.append(result)

    # Aggiungo alla stringa della targa i caratteri che hanno ricevuto i punteggi maggiori nella classificazione
    for prediction in classifications:
        plate += prediction[0]

    print('Predicted license plate (characters may be out of order):')
    print(plate)

    # Riordino i caratteri trovati
    tmp = Segmentation.x_coordinates[:]
    Segmentation.x_coordinates.sort()
    for coordinate in x_chars:
        ordered_plate += plate[tmp.index(coordinate)]

    print('Ordered license plate')
    print(ordered_plate)

import Segmentation
import pickle

print("Loading model...")
filename = './model.sav'
model = pickle.load(open(filename, 'rb'))

print('Model loaded.')
classifications = []

# Ciclo ogni carattere trovato in Segmentation.py
for character in Segmentation.chars:
    # lo converto in un array monodimensionale
    character = character.reshape(1, -1)
    # per passarlo al modello per la prediction
    result = model.predict(character)
    # e aggiungo il risultato ottenuto al vettore dei risultati della classificazione
    classifications.append(result)

# Creo il vettore che conterrà la stringa della targa
plate = ''
# Aggiungo alla stringa della targa i caratteri che hanno ricevuto i punteggi maggiori nella classificazione
for prediction in classifications:
    plate += prediction[0]

print('Predicted license plate (characters may be out of order):')
print(plate)

# Visto che i caratteri potrebbero essere nell'ordine sbagliato, uso la lista x_coordinates creata nel file
# Segmentation.py per riordinarli in base alla posizione (coordinata x) in cui sono stati trovati
tmp = Segmentation.x_coordinates[:]
Segmentation.x_coordinates.sort()
ordered_plate = ''
for coordinate in Segmentation.x_coordinates:
    ordered_plate += plate[tmp.index(coordinate)]

print('Ordered license plate')
print(ordered_plate)

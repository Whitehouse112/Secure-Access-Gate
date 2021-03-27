import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import Detection

# Inverto i pixel bianchi in neri e viceversa della targa trovata in Detection.py
plate = np.invert(Detection.possible_plates[0])

# Ottengo la CCA della targa
labelled = measure.label(plate)

fig, ax1 = plt.subplots(1)
ax1.imshow(plate, cmap="gray")
# nelle targhe italiane i caratteri sono circa il 60% dell'altezza totale della targa, ma col fatto che spesso la targa
# si trova all'ombra che la forma del posteriore delle macchine crea, la targa trovata è possibile che abbia dimensioni
# inferiori a quelle effettive, di conseguenza il carattere occupa più spazio del normale. Il limite massimo è stato
# quindi spostato all'80%, perchè altrimenti caratteri chiaramente visibili sarebbero scartati perchè considerati troppo
# grandi. In largezza questo problema non si pone.
# Nelle targhe italiane un carattere è circa il dieci 10% della larghezza della targa, quindi è stao impostato
# un intervallo tra l'8% e il 12%
char_dims = (0.58*plate.shape[0], 0.80*plate.shape[0], 0.08*plate.shape[1], 0.12*plate.shape[1])
min_h, max_h, min_w, max_w = char_dims

# Vettore di caratteri
chars = []
# Contatore dei caratteri trovati
chars_found = 0
# Liste delle coordinate x (angolo in basso a sinistra) delle regioni che verranno trovate, perchè capita che vengano
# trovate in ordine diverso rispetto a quello effettivo dei carateri nella targa, quindi nel caso questa lista verrà
# utilizzata per riordinarli
x_coordinates = []

# Per ogni regione di un'immagine labellata, regionprops ne restituisce le caratteristiche.
# Ciclo le regioni una per una:
for regions in regionprops(labelled):
    # separo le caratteristiche del bounding box della regione nelle rispettive variabili
    y0, x0, y1, x1 = regions.bbox
    # per ottenere altezza e larghezza della regione
    region_h = y1 - y0
    region_w = x1 - x0

    # Controllo che la regione rispetti le dimensioni che ho imposto sopra, se lo fa, probabilmente è un carattere.
    if min_h < region_h < max_h and min_w < region_w < max_w:
        possible_char = plate[y0:y1, x0:x1]

        # Disegno un rettangolo arancione attorno al carattere trovato
        rectangle = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="orange", linewidth=2, fill=False)
        # Lo aggiungo al plot così poi verrà mostrato
        ax1.add_patch(rectangle)

        # Ridimensiono il carattere a 20x20 visto che le immagini nel dataset hanno quella dimensione
        resized = resize(possible_char, (20, 20))
        # Lo aggiungo alla lista di caratteri
        chars.append(resized)

        # Aggiungo la coordinata x del carattere alla lista dedicata, per riordinare i caratteri se necessario
        x_coordinates.append(x0)
# print(characters)
plt.show()
import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import Detection

def segmentation(possible_plates):

    plate = np.invert(possible_plates[0])

    # Ottengo la CCA della targa
    labelled = measure.label(plate)

    fig, ax1 = plt.subplots(1)
    ax1.imshow(plate, cmap="gray")

    # Limite altezza caratteri: 80% altezza targa
    # Limite larghezza caratteri: tra l'8% ed il 12% della larghezza della targa
    char_dims = (0.58*plate.shape[0], 0.80*plate.shape[0], 0.08*plate.shape[1], 0.12*plate.shape[1])
    min_h, max_h, min_w, max_w = char_dims

    chars = []
    chars_found = 0
    # Lista per rioordinare i caratteri
    x_coordinates = []

    # Per ogni regione di un'immagine labellata, regionprops ne restituisce le caratteristiche.
    for regions in regionprops(labelled):
        # separo le caratteristiche del bounding box della regione nelle rispettive variabili
        y0, x0, y1, x1 = regions.bbox
        # per ottenere altezza e larghezza della regione
        region_h = y1 - y0
        region_w = x1 - x0

        # Controllo che la regione rispetti i limiti di dimensione impostati
        if min_h < region_h < max_h and min_w < region_w < max_w:
            possible_char = plate[y0:y1, x0:x1]

            # Disegno un rettangolo arancione attorno al carattere trovato
            rectangle = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="orange", linewidth=2, fill=False)
            ax1.add_patch(rectangle)

            resized = resize(possible_char, (20, 20))
            chars.append(resized)
            x_coordinates.append(x0)

    plt.show()

    return chars, x_coordinates
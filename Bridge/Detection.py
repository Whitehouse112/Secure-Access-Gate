import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.measure import regionprops


def detection(img):
    # Leggo l'immagine e la converto in scala di grigio.
    gray = imread(img, as_gray=True)

    # Plot 1: da una parte l'immagine in scala di grigio, dall'altra binarizzata.
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(gray, cmap="gray")
    threshold = threshold_otsu(gray)
    binary = gray > threshold
    ax2.imshow(binary, cmap="gray")
    plt.show()

    # Connected Components Analysis: assegnare a pixel vicini con lo stesso valore la stessa label.
    labelled = measure.label(binary)

    # L'altezza della targa deve essere minimo l'8% dell'altezza dell'immagine e massimo il 50%
    # La largezza della targa deve essere minimo il 15% della larghezza dell'immagine e massimo il 50%
    plate_dims = (0.08*labelled.shape[0], 0.5*labelled.shape[0], 0.15*labelled.shape[1], 0.5*labelled.shape[1])
    min_h, max_h, min_w, max_w = plate_dims

    possible_plates = []
    possible_plates_cordinates = []

    # Plot 2: mostra l'immagine in scala di grigio dove la possibile targa sarà circondata da un rettangolo arancione
    fig2, (ax1) = plt.subplots(1)
    ax1.imshow(gray, cmap="gray")

    found_plate = 0
    # Ciclo le regioni una per una:
    for region in regionprops(labelled):
        if region.area < 50:
            continue
        # estraggo altezza e larghezza della regione
        y0, x0, y1, x1 = region.bbox
        region_h = y1 - y0
        region_w = x1 - x0

        # Controllo che la regione rispetti le dimensioni sopra calcolate (region_h, region_w)
        if min_h <= region_h <= max_h and min_w <= region_w <= max_w and region_w > region_h:
            found_plate = 1
            # Aggiungo la regione al vettore di possibili targhe (dall'immagine binarizzata)
            possible_plates.append(binary[y0:y1, x0:x1])
            possible_plates_cordinates.append((y0, x0, y1, x1))
            # Disegno il rettangolo arancione attorno alla possibile targa
            rectangle = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="orange", linewidth=1, fill=False)
            # Lo aggiungo al plot così poi verrà mostrato
            ax1.add_patch(rectangle)

    # Se sono state trovate delle targhe, mostro il plot
    if found_plate == 1:
        plt.show()

    if found_plate == 0:
        print("No plates found")

    return possible_plates
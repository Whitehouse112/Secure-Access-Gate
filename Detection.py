# Per i plot
import matplotlib.pyplot as plt
# Per disegnare il rettangolo attorno alla targa trovata
import matplotlib.patches as patches
# Per leggere le immagini
from skimage.io import imread
# Per l'Otsu thresholding
from skimage.filters import threshold_otsu
# Per etichettare l'immagine con la CCA
from skimage import measure
# Per le regioni nell'immagine
from skimage.measure import regionprops


# L'idea iniziale è di trasformare l'immagine originale prima in scala di grigio e poi binarizzata (solo bianco e nero).
# Leggo l'immagine e la converto in scala di grigio.
gray = imread("input/testFede4.jpg", as_gray=True)


# Per mostrare i passaggi del lavoro fatto, uso dei plot. Se non li si vuole vedere commentare tutti gli
# step, il codice funziona anche senza, è più per debugging per vedere se le cose funzionano quando provo nuove foto.

# Plot 1: da una parte l'immagine in scala di grigio, dall'altra binarizzata.
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray, cmap="gray")
threshold = threshold_otsu(gray)
binary = gray > threshold
ax2.imshow(binary, cmap="gray")
plt.show()

# Il metodo funziona tramite la Connected Components Analysis, cioè assegnare a pixel vicini con lo stesso valore la
# stessa label. Due pixel sono vicini in base al grado di connectivity che si specifica, se non si specifica niente
# come sotto, vuol dire che si intende connettività totale, cioè tutti gli otto pixel intorno a un pixel sono
# considerati suoi vicini
labelled = measure.label(binary)

# L'altezza della targa deve essere minimo l'8% dell'altezza dell'immagine e massimo il 50%
# La largezza della targa deve essere minimo il 15% della larghezza dell'immagine e massimo il 50%
plate_dims = (0.08*labelled.shape[0], 0.5*labelled.shape[0], 0.15*labelled.shape[1], 0.5*labelled.shape[1])
min_h, max_h, min_w, max_w = plate_dims

possible_plates = []
possible_plates_cordinates = []

# Plot 2: per mostrare l'immagine in scala di grigio dove la possibile targa sarà circondata da un rettangolo arancione
fig2, (ax1) = plt.subplots(1)
ax1.imshow(gray, cmap="gray")

found_plate = 0
# Per ogni regione di un'immagine labellata, regionprops ne restituisce le caratteristiche.
# Ciclo le regioni una per una:
for region in regionprops(labelled):
    # Se l'area della regione è troppo piccola probabilmente non è una targa
    if region.area < 50:
        continue
    # separo le caratteristiche del bounding box della regione nelle rispettive variabili
    y0, x0, y1, x1 = region.bbox
    # per ottenere altezza e larghezza della regione
    region_h = y1 - y0
    region_w = x1 - x0

    # Controllo che la regione rispetti le dimensioni che ho imposto sopra, se lo fa, probabilmente è una targa.
    if min_h <= region_h <= max_h and min_w <= region_w <= max_w and region_w > region_h:
        found_plate = 1
        # Aggiungo la regione al vettore di possibili targhe, prendendola però dall'immagine binarizzata
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

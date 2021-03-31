from lof import LOF
from matplotlib import pyplot as p
import numpy as np

# Calcolo lof per le coordinate geografiche

# Punti presi a caso nell'intorno di pochi metri di un cancello di una casa random
geographic_coordinates = [
 (44.773647, 10.874154),
 (44.773658, 10.874135),
 (44.773686, 10.874191),
 (44.773623, 10.874142),
 (44.773630, 10.874144),
 (44.773679, 10.874174),
 (44.773654, 10.874218),
 (44.773674, 10.874135),
 (44.773640, 10.874202)]

lof = LOF("geodesic_distance", geographic_coordinates)

# Esempi di outliers: punti presi a una casa di distanza, tre case di distanza, una via parallela
for instance in [[44.773564, 10.874451], [44.773406, 10.874851], [44.774288, 10.874526]]:
    # Per ogni istanza mi faccio tornare il valore di lof, se è >=1 il punto è outlier e lo coloro di rosso
    # e lo faccio più grande più è ourlier, se è <1 è inlier e lo faccio verde
    value = lof.local_outlier_factor(3, instance)
    print(value, instance)
    color = "#FF0000" if value > 1 else "#00FF00"
    p.scatter(instance[0], instance[1], color=color, s=(value - 1) ** 2 * 10 + 20)

# Disegno anche i punti forniti come coordinate del cancello in blu
x,y = zip(*geographic_coordinates)
p.scatter(x,y, 9, color="#0000FF")

p.show()
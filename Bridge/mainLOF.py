from lof import LOF
from matplotlib import pyplot as p

# Calcolo lof per le coordinate geografiche

# Punti presi a caso nell'intorno di pochi metri di un cancello di una casa random
geographic_coordinates = [
 (44.77364720217285, 10.874154166188879),
 (44.77365862668815, 10.874135390728647),
 (44.77368623592409, 10.874191717116714),
 (44.77362340109209, 10.874142096251035),
 (44.77363054141734, 10.874144107907751),
 (44.77367909560573, 10.874174953310744),
 (44.77365481851662, 10.874218539206272),
 (44.77367481141427, 10.874135390728647),
 (44.77364050064099, 10.874202428716771)]

lof = LOF("geodesic_distance", geographic_coordinates)

# Esempi di outliers: punti presi a una casa di distanza, tre case di distanza, una via parallela
for instance in [[44.77356433519205, 10.87445184529774], [44.77340629559869, 10.87485149443705], [44.77428822057317, 10.87452670388886]]:
    value = lof.local_outlier_factor(3, instance)
    print(value, instance)

x,y = zip(*geographic_coordinates)
p.scatter(x,y, 9, color="#0000FF")

# Uguale ma per il grafico
for instance in [[44.77356433519205, 10.87445184529774], [44.77340629559869, 10.87485149443705], [44.77428822057317, 10.87452670388886]]:
    value = lof.local_outlier_factor(3, instance)
    color = "#FF0000" if value > 1 else "#00FF00"
    p.scatter(instance[0], instance[1], color=color, s=(value-1)**2*10+20)

p.show()
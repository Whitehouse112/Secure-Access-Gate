import re
from lof import LOF


def convertInMinutes(datetime):
    h = re.search(' (.*?):', datetime)
    hours = int(h.group(1))
    min = re.search(':(.*):', datetime)
    minutes = int(min.group(1))
    return hours*60+minutes


def anomalyDetection(activities_list, new_activity):
    opening_times_in_minutes = []
    positions = []
    for a in activities_list:
        opening_times_in_minutes.append((convertInMinutes(a['date_time']), 0))
    lofTimes = LOF("euclidean_distance", opening_times_in_minutes, normalize=False)

    timeToCheck = convertInMinutes(new_activity['date_time'])
    timeAnomaly = lofTimes.local_outlier_factor(3, (timeToCheck, 0))
    if timeAnomaly > 1:
        return timeAnomaly
    else:
        for a in activities_list:
            positions.append(a['position'])
        lofPositions = LOF("geodesic_distance", positions, normalize=False)

        posistionAnomaly = lofPositions.local_outlier_factor(3, new_activity['position'])
        if posistionAnomaly > 1:
            return posistionAnomaly
        else:
            return 0


# Codice che crea attività d'esempio per mostrare che la funzione sopra funziona,
# nel codice del progetto basterà chiamare la funzione anomalyDetection passandogli la lista
# di attività dell'utente e la nuova attività da controllare.

# Lista di dizionari, ogni dizionario è un'attività
activities = [
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 08:00:00",
    'position': (44.773647, 10.874154),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 08:02:00",
    'position': (44.773658, 10.874135),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 08:05:00",
    'position': (44.773686, 10.874191),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 07:54:00",
    'position': (44.773623, 10.874142),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 07:57:00",
    'position': (44.773630, 10.874144),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 18:30:00",
    'position': (44.773679, 10.874174),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 18:33:00",
    'position': (44.773654, 10.874218),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 18:27:00",
    'position': (44.773674, 10.874135),
    'outcome': "Granted"
},
{
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 18:25:00",
    'position': (44.773640, 10.874202),
    'outcome': "Granted"
}
]

# Due esempi anomali
activity_anomalaOrario = {
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 02:48:00",
    'position': (44.773640, 10.874202),
    'outcome': "Granted"
}

activity_anomalaPosizione = {
    'id_user': 123,
    'id_gate': 456,
    'id_car': 'fb190gy',
    'date_time': "2021/04/07 08:00:00",
    'position': (45.773640, 10.874202),
    'outcome': "Granted"
}

anomaly = anomalyDetection(activities, activity_anomalaPosizione)
print(anomaly)

import re
from lof import LOF
from datetime import datetime

class AnomalyDetection():

    def convertInMinutes(self, datetime):
        h = re.search(' (.*?):', datetime)
        hours = int(h.group(1))
        min = re.search(':(.*):', datetime)
        minutes = int(min.group(1))
        return hours*60+minutes


    def detect(self, activities_list):

        opening_times_in_minutes = []
        positions = []

        now = datetime.now()
        date_time = now.strftime("%Y/%m/%g %H:%M:%S")

        for a in activities_list:
            opening_times_in_minutes.append((convertInMinutes(a['date_time']), 0))
        lofTimes = LOF("euclidean_distance", opening_times_in_minutes, normalize=False)

        timeToCheck = convertInMinutes(date_time)
        timeAnomaly = lofTimes.local_outlier_factor(3, (timeToCheck, 0))
        if timeAnomaly > 1:
            return timeAnomaly
        else:
            # for a in activities_list:
            #     positions.append(a['position'])
            # lofPositions = LOF("geodesic_distance", positions, normalize=False)

            # posistionAnomaly = lofPositions.local_outlier_factor(3, new_activity['position'])
            # if posistionAnomaly > 1:
            #     return posistionAnomaly
            # else:
            return 0

    # Codice che crea attività d'esempio per mostrare che la funzione sopra funziona,
    # nel codice del progetto basterà chiamare la funzione anomalyDetection passandogli la lista
    # di attività dell'utente e la nuova attività da controllare.

    # Lista di dizionari, ogni dizionario è un'attività
    # activities = [
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 08:00:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 08:02:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 08:05:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 07:54:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 07:57:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 18:30:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 18:33:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 18:27:00",
    #     'outcome': "Granted"
    # },
    # {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 18:25:00",
    #     'outcome': "Granted"
    # }
    # ]

    # # Due esempi anomali
    # activity_anomalaOrario = {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 02:48:00",
    #     'outcome': "Granted"
    # }

    # activity_anomalaPosizione = {
    #     'id_user': 123,
    #     'id_gate': 456,
    #     'id_car': 'fb190gy',
    #     'date_time': "2021/04/07 08:00:00",
    #     'outcome': "Granted"
    # }

    # anomaly = anomalyDetection(activities, activity_anomalaPosizione)
    # print(anomaly)

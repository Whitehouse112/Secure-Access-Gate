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


    def detect_dateTime(self, activities_list):


        now = datetime.now()
        date_time = now.strftime("%Y/%m/%g %H:%M:%S")

        opening_times_in_minutes = [(convertInMinutes(x['date_time']), 0) for x in activities_list]
        lofTimes = LOF("euclidean_distance", opening_times_in_minutes, normalize=False)

        timeToCheck = convertInMinutes(date_time)
        timeAnomaly = lofTimes.local_outlier_factor(3, (timeToCheck, 0))
        if timeAnomaly > 1:
            return timeAnomaly
        else:
            return 0

    def detect_locations(self, locations_list, current_location):

        current_location = tuple(current_location['Latitude'] + current_location['Longitude'])
        locations = [tuple(x['Latitude'] + x['Longitude']) for x in locations_list]

        if locations[0] != current_location:
            return 1

        #TODO: controllare le posizioni passate
        # return 1 se c'è errore
        # return 0 altrimenti
        return 0
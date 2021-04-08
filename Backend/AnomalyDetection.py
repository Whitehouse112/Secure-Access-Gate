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
            return 0

    def detect_locations(self, locations_list, current_location):
        print("prova")
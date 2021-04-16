import re
import requests
from lof import LOF
from datetime import datetime
from geopy import distance

API_Key = "AIzaSyC7djHwQhw4eb0hR33wAkW5oclmyp6BaUA"

class AnomalyDetection():

    def convertInMinutes(self, datetime):
        
        h = re.search(' (.*?):', datetime)
        hours = int(h.group(1))
        min = re.search(':(.*):', datetime)
        minutes = int(min.group(1))
        return hours*60+minutes


    def detect_dateTime(self, activities_list):

        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

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
        times = [x['Date_Time'] for x in locations_list]

        gate_distance = distance.distance(current_location, locations[0]).kilometers
        if gate_distance > 0.5:
            return 1

        tmp = 0
        for i in range(3):
            # calcolo intervallo di tempo tra la posizione i+1 ed i
            driving_time = datetime.strptime(times[i+1], "%Y-%m-%d %H:%M:%S") - datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
            driving_time = driving_time.total_seconds()
            
            # calcolo il tempo di percorrenza tra i punti i ed i+1
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={str(locations[i][0])},{str(locations[i][1])}&destinations={str(locations[i+1][0])},{str(locations[i+1][1])}&mode=driving&language=en-EN&sensor=false&key={API_Key}"
            result = requests.get(url).json()
            expecting_time = result['rows'][0]['elements'][0]['duration']['value']

            # controllo che il tempo impiegato sia compatibile con il tempo stimato di percorrenza (30% di scarto)
            if  (driving_time < expecting_time*0.70) or (driving_time > expecting_time*1.30): 
                tmp = 1
                break
        return tmp
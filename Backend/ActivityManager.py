import database
import sqlalchemy
from datetime import datetime

class ActivityManager():

    def __init__(self):
        self.db = database.create_connection()

    def getLastActivity(self, id_user, id_gate, status):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Accesses WHERE ID_User=:id_user and ID_Gate=:id_gate and Outcome=:outcome order by Date_Time DESC")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate, outcome=status).fetchone()
        except Exception as e:
            return 500

    def getActivities(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("select A.ID_User, A.ID_Gate, C.Plate as ID_Car, A.Date_Time, A.Outcome, A.Photo" + 
                                        " from Accesses as A, Cars as C where A.ID_User=:id_user and A.ID_Car=C.ID")
                activities = conn.execute(stmt, id_user=id_user).fetchall()
                ret = []
                for activity in activities:
                    activity_info = {}
                    for field in activity.__getattribute__('_fields'):
                        data = activity.__getattribute__(field)
                        if field == 'Date_Time':
                            data = data.strftime("%Y-%m-%d %H:%M:%S")
                        activity_info[field] = data
                    ret.append(activity_info)
                return ret
        except Exception as e:
            return 500

    def addActivity(self, id_user, id_gate, id_car, outcome, photo):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Accesses VALUES (:id_user, :id_gate, :id_car, :date_time, :outcome, :photo)")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate, id_car=id_car, date_time=date_time, outcome=outcome, photo=photo)
        except Exception as e:
            return 500

    def getGuestsActivities(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("select A.ID_User, A.ID_Gate, C.Plate as ID_Car, A.Date_Time, A.Outcome, A.Photo" + 
                                        " from Guests_Accesses as A, Cars as C where A.ID_User=:id_user and A.ID_Car=C.ID")
                activities = conn.execute(stmt, id_user=id_user).fetchall()
                ret = []
                for activity in activities:
                    activity_info = {}
                    for field in activity.__getattribute__('_fields'):
                        data = activity.__getattribute__(field)
                        if field == 'Date_Time':
                            data = data.strftime("%Y-%m-%d %H:%M:%S")
                        activity_info[field] = data
                    ret.append(activity_info)
                return ret
        except Exception as e:
            return 500

    def addGuestActivity(self, id_user, id_gate, id_car, outcome, photo):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Guests_Accesses VALUES (:id_user, :id_gate, :id_car, :date_time, :outcome, :photo)")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate, id_car=id_car, date_time=date_time, outcome=outcome, photo=photo)
        except Exception as e:
            return 500

    def updateActivity(self, id_user, id_gate, date_time, status, outcome):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Accesses SET Outcome=:outcome WHERE ID_User=:id_user and ID_Gate=:id_gate and Date_Time=:date_time and Outcome=:status")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate, date_time=date_time, status=status, outcome=outcome)
        except Exception as e:
            return 500

class Activity:
    def __init__(self, gateId, licensePlate, color, date):
        self.gateId = gateId
        self.licensePlate = licensePlate
        self.color = color
        self.date = date

    def __repr__(self):
        return f'<Gate ID: {self.gateId}>'
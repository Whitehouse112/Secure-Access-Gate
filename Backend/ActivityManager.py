import database
import sqlalchemy
from datetime import datetime

class ActivityManager():

    def __init__(self):
        self.db = database.create_connection()

    def getActivities(self, id_user, id_gate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Accesses WHERE ID_User=:id_user and ID_Gate=:id_gate")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate).fetchall()
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

    def addGuestActivity(self, id_user, id_gate, id_car, outcome, photo):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Guests_Accesses VALUES (:id_user, :id_gate, :id_car, :date_time, :outcome, :photo)")
                return conn.execute(stmt, id_user=id_user, id_gate=id_gate, id_car=id_car, date_time=date_time, outcome=outcome, photo=photo)
        except Exception as e:
            return 500

class Activity:
    def __init__(self, gateId, licensePlate, color, date):
        self.gateId = gateId
        self.licensePlate = licensePlate
        self.color = color
        self.date = date

    def __repr__(self):
        #TODO: complete when you have the definitive form for the access object
        return f'<Gate ID: {self.gateId}>'
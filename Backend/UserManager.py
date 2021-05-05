from werkzeug.security import generate_password_hash, check_password_hash
import database
import sqlalchemy
from datetime import datetime

class UserManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkGate(self, id_gate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT ID_User FROM Gates WHERE ID=:id_gate")
                return conn.execute(stmt, id_gate=id_gate).fetchone()
        except Exception as e:
            return 500

    def checkUser(self, email):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Users WHERE Email=:email")
                return conn.execute(stmt, email=email).fetchone()
        except Exception as e:
            return 500

    def getUser(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Users WHERE ID=:id_user")
                user = conn.execute(stmt, id_user=id_user).fetchone()
                ret = {}
                for field in user.__getattribute__('_fields'):
                    data = user.__getattribute__(field)
                    ret[field] = data
                return ret
        except Exception as e:
            return 500

    def addUser(self, email, password):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Users (Email, Pwd) VALUES (:email, :pwd)")
                return conn.execute(stmt, email=email, pwd=password)
        except Exception as e:
            return 500

    def checkGuest(self, id_car):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Guests WHERE ID_Car=:id_car")
                return conn.execute(stmt, id_car=id_car).fetchone()
        except Exception as e:
            return 500

    def getGuests(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Guests WHERE ID_Administrator=:id_user")
                guests = conn.execute(stmt, id_user=id_user).fetchall()
                ret = []
                for guest in guests:
                    guest_info = {}
                    for field in guest.__getattribute__('_fields'):
                        data = guest.__getattribute__(field)
                        if field == 'Date_Time':
                            data = data.strftime("%Y-%m-%d %H:%M:%S")
                        guest_info[field] = data
                    ret.append(guest_info)
                return ret
        except Exception as e:
            return 500

    def addGuest(self, id_user, id_car, dead_line, nickname):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Guests VALUES (:id_user, :id_car, :dead_line, :nickname)")
                return conn.execute(stmt, id_user=id_user, id_car=id_car, dead_line=dead_line, nickname=nickname)
        except Exception as e:
            return 500

    def loginUser(self, email, jwt_refresh):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Users SET Jwt_refresh=:jwt_refresh WHERE Email=:email")
                return conn.execute(stmt, jwt_refresh=jwt_refresh, email=email)
        except Exception as e:
            return 500

    def logoutUser(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Users SET Jwt_refresh=NULL WHERE ID=:id_user")
                return conn.execute(stmt, id_user=id_user)
        except Exception as e:
            return 500

    def updateLocation(self, id_user, latitude, longitude):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Users_Location VALUES (:id_user, :date_time, :latitude, :longitude)")
                return conn.execute(stmt, id_user=id_user, date_time=date_time, latitude=latitude, longitude=longitude)
        except Exception as e:
            return 500
    
    def getLocations(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT TOP 5 * FROM Users_Location WHERE ID=:id_user order by Date_Time desc")
                return conn.execute(stmt, id_user=id_user)
        except Exception as e:
            return 500

    def updateFCM(self, id_user, fcm_token):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Users SET FCM_token=:fcm_token where ID=:id_user")
                return conn.execute(stmt, id_user=id_user, fcm_token= fcm_token)
        except Exception as e:
            return 500

class User:
    def __init__(self, id, email, password, jwt_refresh):
        self.id = id
        self.email = email
        self.password = password
        self.jwt_refresh = jwt_refresh

    def __repr__(self):
        return f'<User:>'
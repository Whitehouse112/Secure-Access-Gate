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

    def getUser(self, id):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Users WHERE ID=:id")
                return conn.execute(stmt, id=id).fetchone()
        except Exception as e:
            return 500

    def addUser(self, email, password):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Users (Email, Pwd) VALUES (:email, :pwd)")
                return conn.execute(stmt, email=email, pwd=password)
        except Exception as e:
            return 500

    def loginUser(self, email, jwt_refresh):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Users SET Jwt_refresh=:jwt_refresh where Email=:email")
                return conn.execute(stmt, jwt_refresh=jwt_refresh, email=email)
        except Exception as e:
            return 500

    def logoutUser(self, id):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("UPDATE Users SET Jwt_refresh=NULL where ID=:id")
                return conn.execute(stmt, id=id)
        except Exception as e:
            return 500

    def updateLocation(self, id_user, location):
        now = datetime.now()
        date_time = now.strftime("%Y/%m/%g %H:%M:%S")
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Users_Location VALUES (:id_user, :date_time, :location)")
                return conn.execute(stmt, id_user=id_user, date_time=date_time, location=location)
        except Exception as e:
            return 500

class User:
    def __init__(self, id, email, password, jwt_refresh):
        self.id = id
        self.email = email
        self.password = password
        self.jwt_refresh = jwt_refresh

    def __repr__(self):
        #TODO: complete when you have the definitive form for the user object
        return f'<User:>'
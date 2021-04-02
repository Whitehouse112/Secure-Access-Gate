from werkzeug.security import generate_password_hash, check_password_hash
import database
import sqlalchemy


class UserManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkPassword(self, password):
        #TODO: check for user password
        return True

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

    def checkLocation(self, location):
        #TODO: check if location is already used (in particular datetime timestamp)
        return True

    def updateLocation(self, location):
        #TODO: update location of the user
        print(location)
        return True

    def checkCar(self, id_user, license_plate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Cars WHERE Plate=:license_plate and ID_User =:id_user ")
                return conn.execute(stmt, license_plate=license_plate, id_user=id_user).fetchone()
        except Exception as e:
            return 500

    def addCar(self, id_user, license_plate, color, brand):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Cars VALUES (Plate=:license_plate, Color=:color, Brand=:brand, ID_User =:id_user)")
                return conn.execute(stmt, license_plate=license_plate, color=color, brand=brand, id_user=id_user)
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
import database
import sqlalchemy

class CarManager:

    def __init__(self):
        self.db = database.create_connection()

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
                stmt = sqlalchemy.text("INSERT INTO Cars VALUES (:license_plate, :color, :brand, :id_user)")
                return conn.execute(stmt, license_plate=license_plate, color=color, brand=brand, id_user=id_user)
        except Exception as e:
            return 500

class Car:
    def __init__(self, id, license_plate, color, brand):
        self.id = id
        self.license_plate = license_plate
        self.color = color
        self.brand = brand

    def __repr__(self):
        #TODO: complete when you have the definitive form for the user object
        return f'<User:>'
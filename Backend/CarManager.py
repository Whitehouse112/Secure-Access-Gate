import database
import sqlalchemy

class CarManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkCar(self, id_user, license_plate, color):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Cars WHERE Plate=:license_plate and ID_User =:id_user and color=:color")
                return conn.execute(stmt, license_plate=license_plate, id_user=id_user, color=color).fetchone()
        except Exception as e:
            return 500

    def getCars(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Cars WHERE ID_User =:id_user")
                cars = conn.execute(stmt, id_user=id_user).fetchall()
                ret = []
                for car in cars:
                    car_info = {}
                    for field in car.__getattribute__('_fields'):
                        data = car.__getattribute__(field)
                        car_info[field] = data
                    ret.append(car_info)
                return ret
        except Exception as e:
            return 500

    def addCar(self, id_user, license_plate, color, brand):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Cars VALUES (:license_plate, :brand, :color, :id_user)")
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
        return f'<User:>'
import database
import sqlalchemy

class GateManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkSensors(self, id_gate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Sensors WHERE ID=:id_gate")
                return conn.execute(stmt, id_gate=id_gate).fetchone()
        except Exception as e:
            return 500

    def checkGate(self, id_user, id_gate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Gates WHERE ID=:id_gate and ID_User=:id_user")
                return conn.execute(stmt, id_gate=id_gate, id_user=id_user).fetchone()
        except Exception as e:
            return 500

    def getGates(self, id_user):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Gates WHERE ID_User=:id_user")
                gates = conn.execute(stmt, id_user=id_user).fetchall()
                ret = []
                for gate in gates:
                    gate_info = {}
                    for field in gate.__getattribute__('_fields'):
                        if field == 'Latitude' or field == 'Longitude':
                            continue
                        data = gate.__getattribute__(field)
                        gate_info[field] = data
                    ret.append(gate_info)
                return ret
        except Exception as e:
            return 500

    def addGate(self, id_user, id_gate, name, location, latitude, longitude, photo):
        try:
            with self.db.connect() as conn:
                if photo is None:
                    stmt = sqlalchemy.text("INSERT INTO Gates (ID, ID_User, Name, Location, Latitude, Longitude) VALUES (:id_gate, :id_user, :name, :location, :latitude, :longitude)")
                    return conn.execute(stmt, id_gate=id_gate, id_user=id_user, name=name, location=location, latitude=latitude, longitude=longitude)
                else:
                    stmt = sqlalchemy.text("INSERT INTO Gates VALUES (:id_gate, :id_user, :name, :location, :latitude, :longitude, :photo)")
                    return conn.execute(stmt, id_gate=id_gate, id_user=id_user, name=name, location=location, latitude=latitude, longitude=longitude, photo=photo)
        except Exception as e:
            return 500

class Gate:
    def __init__(self, id, location, photo):
        self.id = id
        self.location = location
        self.photo = photo

    def __repr__(self):
        return f'<Gate: {self.name}>'
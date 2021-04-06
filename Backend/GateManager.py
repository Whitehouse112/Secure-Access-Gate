import database
import sqlalchemy

class GateManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkSensors(self, id_gate):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT * FROM Sensors where ID=:id_gate")
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
                return conn.execute(stmt, id_user=id_user).fetchall()
        except Exception as e:
            return 500

    def addGate(self, id_user, id_gate, name, location):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("INSERT INTO Gates (ID, ID_User, Name, Location) VALUES (:id_gate, :id_user, :name, :location)")
                return conn.execute(stmt, id_gate=id_gate, id_user=id_user, name=name, location=location)
        except Exception as e:
            return 500

class Gate:
    def __init__(self, id, location, photo):
        self.id = id
        self.location = location
        self.photo = photo

    def __repr__(self):
        #TODO: complete when you have the definitive form for the gate object
        return f'<Gate: {self.name}>'
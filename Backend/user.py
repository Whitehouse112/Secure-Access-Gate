from werkzeug.security import generate_password_hash, check_password_hash
import database
import sqlalchemy


class UserManager:

    def __init__(self):
        self.db = database.create_connection()

    def checkUser(self, email):
        try:
            with self.db.connect() as conn:
                stmt = sqlalchemy.text("SELECT email FROM Users WHERE email =:email")
                return conn.execute(stmt, email=email).fetchone()
        except Exception as e:
            return 500

    def checkPassword(self, password):
        #TODO: check for user password
        return True

    def getUser(self, email, pwd):
        stmt = "SELECT email, pwd from Users where email=:email and pwd=:pwd"
        return  db.insert(stmt, email, pwd)
        #TODO: get all the informations abount the user
        #return User(1, 'Antonio', generate_password_hash('password', method='sha256'))

    def addUser(self, email, password):
        pass

    def logoutUser(self, userId):
        #TODO: logout user, aka delete refresh token
        return True

    def checkLocation(self, location):
        #TODO: check if location is already used (in particular datetime timestamp)
        return True

    def updateLocation(self, location):
        #TODO: update location of the user
        print(location)
        return True

class User:
    def __init__(self, id, email, password, jwt_refresh):
        self.id = id
        self.email = email
        self.password = password
        self.jwt_refresh = jwt_refresh

    def __repr__(self):
        #TODO: complete when you have the definitive form for the user object
        return f'<User:>'
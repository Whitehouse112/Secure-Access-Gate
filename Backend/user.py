from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    def checkUser(self, userId):
        #TODO: check if user in DB
        return True

    def checkPassword(self, password):
        #TODO: check for user password
        return True

    def getUser(self, userId):
        #TODO: get all the informations abount the user
        return User(1, 'Antonio', generate_password_hash('password', method='sha256'))

    def logoutUser(self, userId):
        #TODO: logout user, aka delete refresh token
        return True

    def checkLocation(self, location):
        #TODO: check if location is already used (in particular datetime timestamp)
        return True

    def updateLocation(self, location):
        #TODO: update location of the user
        return True

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        #TODO: complete when you have the definitive form for the user object
        return f'<User: {self.user}>'
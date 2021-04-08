import jwt
import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from activityManager import ActivityManager
from anomalyDetection import AnomalyDetection
from carManager import CarManager
from gateManager import GateManager
from userManager import UserManager
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import pubsub

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'

activityManager = ActivityManager()
anomalyDetection = AnomalyDetection()
carManager = CarManager()
gateManager = GateManager()
userManager = UserManager()

STATUS = ['granted', 'denied', 'ignored', 'pending', 'reported']
COLOR = ['Black', 'Blue', 'Green', 'Gray', 'Red', 'White', 'Yellow', 'Cyan']

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return "Token is missing or invalid", 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return "Token is missing or invalid", 401

        return f(*args, current_user, **kwargs)

    return decorated

class ActivityAPI(Resource):
    def post(self):

        id_gate = request.get_json()['id_gate']
        license_plate = request.get_json()['license']
        color = request.get_json()['color']
        #TODO: attività: leggere campo foto (photo = request.get_json()['photo'])
        
        if  gateManager.checkSensors(id_gate) is None:
            return "Invalid input data", 400
        if license_plate is None or len(license_plate) != 7:
            return "Invalid input data", 400
        if color not in COLOR:
            return "Invalid input data", 400

        user = userManager.checkGate(id_gate)[0]
        if user == 500:
            return 'Internal server error', 500
        if user is None:
            return 'User not found', 404

        car = carManager.checkCar(user, license_plate, color)
        if car == 500:
            return 'Internal server error', 500
        if car is None:
            return 'Car not found', 404

        # ottengo la lista di attività dell'utente e controllo le
        # anomalie in termini di incongruenze con data e ora
        activities = activityManager.getActivities(user, id_gate)
        if activities == 500:
            return 'Internal server error', 500
        if len(activities) < 5:
            time_anomaly = 0
        else:
            time_anomaly = anomalyDetection.detect_dateTime(activities)

        if time_anomaly == 0:
            # ottengo la lista delle ultime posizioni dell'utente e controllo le
            # anomalie in termini di incongruenze con l'attuale posizione
            current_location = gateManager.checkGate(user, id_gate)['Location']
            if current_location is None:
                return "Gate not found", 404
            locations = userManager.getLocations(user)
            if locations == 500:
                return 'Internal server error', 500
            if len(locations) < 5:
                location_anomaly = 0
            else:
                location_anomaly = anomalyDetection.detect_locations(locations, current_location)
        else:
            location_anomaly = 0

        # controllo se sono state rilevate o meno delle anomalie
        if time_anomaly >= 1 or location_anomaly == 1:
            outcome = 'Pending'
            ret_code = 202
            #TODO: notificare l'utente a seguito della richiesta di Pending
        else:
            outcome = 'Granted'
            ret_code = 200
        
        #TODO: aggiungere foto al cloud ed ottenere il link
        #TODO: aggiungere campo photo alla funzione addActivity
        ret = activityManager.addActivity(user, id_gate, car['ID'], outcome)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return outcome, ret_code
        
    # @token_required
    # def put(self, current_user):
        
    #     activityId = request.get_json()['activityId']
    #     userId = request.get_json()['userId']
    #     status = request.get_json()['status']

    #     if activity.checkActivity(userId, activityId):
    #         return "No Activity found", 404

    #     if status not in STATUS:
    #         return "Invalid input data", 400

    #     if activity.updateActivity(userId, activityId, status):
    #         return "Internal server error", 500
    #     else:
    #         return "Success", 200

    # @token_required
    # def get(current_user, self):
        
    #     if not userManager.checkUser(current_user):
    #         return "Invalid input data", 400

    #     ret = activity.getActivity(current_user)
    #     if ret != []:
    #         return ret, 200
    #     else:
    #         return "No Gate found", 404

class CarAPI(Resource):
    @token_required
    def post(self, current_user):
        
        license_plate = request.get_json()['license']
        color = request.get_json()['color']
        brand = request.get_json()['brand']

        if license_plate is None or len(license_plate) != 7:
            return "Invalid input data", 400
        if color not in COLOR:
            return "Invalid input data", 400

        #TODO: eventualmente controllare anche il brand
        car = carManager.checkCar(current_user, license_plate, color)
        if car == 500:
            return 'Server error', 500
        if car is not None:
            return "Car already exists", 409

        ret = carManager.addCar(current_user, license_plate, color, brand)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return 'Success', 200

class GateAPI(Resource):
    @token_required
    def post(self, current_user):
        
        id_gate = request.get_json()['id_gate']
        name = request.get_json()['name']
        location = request.get_json()['location']
        latitude = request.get_json()['latitude']
        longitude = request.get_json()['longitude']
        #TODO: gate: leggere campo foto (photo = request.get_json()['photo'])

        if id_gate is None:
            return "Invalid input data", 400
        if gateManager.checkSensors(id_gate) is None:
            return "Invalid input data", 400
        if name is None:
            return "Invalid input data", 400
        if location is None:
            return "Invalid input data", 400
        if latitude is None:
            return "Invalid input data", 400
        if longitude is None:
            return "Invalid input data", 400

        gate = gateManager.checkGate(current_user, id_gate)
        if gate == 500:
            return 'Server error', 500
        if gate is not None:
            return 'Gate already exists', 409

        #TODO: aggiungere foto al cloud ed ottenere il link
        #TODO: aggiungere campo foto alla funzione addGate
        ret = gateManager.addGate(current_user, id_gate, name, location, latitude, longitude)
        if ret == 500:
            return 'Internal server error', 500
        else:
            pubsub.createTopic(id_gate)
            return 'Success', 200

    @token_required
    def get(self, current_user):

        gates = gateManager.getGates(current_user)
        if gates is None:
            return "No Gate found", 404
        if gates == 500:
            return "Server error", 500
        else:
            return jsonify(gates)

class OpenGateAPI(Resource):
    @token_required
    def post(self, current_user):

        id_gate = request.get_json()['id_gate']
        if id_gate is None:
            return "Invalid input data", 400
        if gateManager.checkSensors(id_gate) is None:
            return "Invalid input data", 400

        pubsub.publishTopic(id_gate)
        return "Success", 200

class RefreshJWT(Resource):
    def post(self):
        
        token = request.get_json()['jwt_refresh']
        if not token:
            return "Invalid input data", 400

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']

            user = userManager.getUser(current_user)
            if user is None:
                return "User not found", 404
            if (user['Jwt_refresh'] != token):
                return "Token is invalid", 401
        except:
            return "Token is invalid", 401
        
        jwt_expiry = jwt.encode({'user':current_user, 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'jwt_token_expiry':jwt_expiry})

class SigninUser(Resource):
    def post(self):
        
        content = request.get_json()
        user = userManager.checkUser(content['email'])
        if user == 500:
            return 'Server error', 500
        if user is not None:
            return 'User already exists', 409

        hashed_password = generate_password_hash(content['password'], method='sha256') 
        ret = userManager.addUser(content['email'], hashed_password)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return 'Success', 200

class LoginUser(Resource):
    def get(self):
        
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return "Invalid input data", 400
        
        user = userManager.checkUser(auth.username)
        if user is None:
            return "Invalid username/password supplied", 401

        if check_password_hash(user['Pwd'], auth.password):
            jwt_refresh = jwt.encode({'user':user['ID'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=30)}, app.config['SECRET_KEY'])   
            jwt_expiry = jwt.encode({'user':user['ID'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])

            ret = userManager.loginUser(auth.username, jwt_refresh)
            if ret == 500:
                return 'Internal server error', 500
            return jsonify({'jwt_token':jwt_refresh, 'jwt_token_expiry':jwt_expiry})
        else:
            return "Invalid username/password supplied", 401

class LogoutUser(Resource):
    @token_required
    def get(self, current_user):
        
        user = userManager.getUser(current_user)
        if user == 500:
            return "Server error", 500
        if user is None:
            return "User not found", 404 

        ret = userManager.logoutUser(current_user)
        if ret == 500:
            return "Internal server error", 500
        else:
            return 'Success', 200
            
class UpdateLocation(Resource):
    @token_required
    def post(self, current_user):

        latitude = request.get_json()['latitude']
        longitude = request.get_json()['longitude']
        if latitude is None:
            return "Invalid input data", 400
        if longitude is None:
            return "Invalid input data", 400

        user = userManager.getUser(current_user)
        if user == 500:
            return "Server error", 500
        if user is None:
            return "User not found", 404 

        ret = userManager.updateLocation(current_user, latitude, longitude)
        if ret == 500:
            return "Internal server error", 500
        else:
            return "Success", 200
            
api.add_resource(ActivityAPI, f'{basePath}/activity')
api.add_resource(CarAPI, f'{basePath}/car')
api.add_resource(GateAPI, f'{basePath}/gate')
api.add_resource(OpenGateAPI, f'{basePath}/gate/open')
api.add_resource(RefreshJWT, f'{basePath}/jwt')
api.add_resource(SigninUser, f'{basePath}/user/signin')
api.add_resource(LoginUser, f'{basePath}/user/login')
api.add_resource(LogoutUser, f'{basePath}/user/logout')
api.add_resource(UpdateLocation, f'{basePath}/user/location')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
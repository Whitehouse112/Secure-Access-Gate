from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import jwt
import datetime
from GateManager import GateManager
from CarManager import CarManager
from UserManager import UserManager
from ActivityManager import ActivityManager
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'

gateManager = GateManager()
userManager = UserManager()
activityManager = ActivityManager()
carManager = CarManager()

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
            #TODO: correct with actual user db information
            #current_user = userManager.getUser(data['user'])
            current_user = data['user']
        except:
            return "Token is missing or invalid", 401

        return f(current_user, *args, **kwargs)

    return decorated

class ActivityAPI(Resource):
    def post(self):

        id_gate = request.get_json(['id_gate'])
        license_plate = request.get_json()['license']
        color = request.get_json()['color']
        
        if id_gate not in gateManager.checkSensors():
            return "Invalid input data", 400
        if license_plate is None or len(license_plate) != 7:
            return "Invalid input data", 400
        if color not in COLOR:
            return "Invalid input data", 400

        user = userManager.checkGate(id_gate)
        if user == 500:
            return 'Internal server error', 500
        if user is None:
            return 'User not found', 404

        cars = carManager.checkCar(user, license_plate, color)
        if cars == 500:
            return 'Internal server error', 500
        if cars is None:
            return 'Car not found', 404

        activities = activityManager.getActivities(user, id_gate)
        if activities == 500:
            return 'Internal server error', 500
        
        if len(activities) < 10:
            anomaly = 1
        else:
            # anomaly detection con la lista di attività sulla base del datetime
            # controllare le attività dell'utente tramite anomaly detection
            # anomaly = anomalyDetecion(activities)
            anomaly = 2

        if anomaly > 1:
            outcome = 'Pending'
            ret_code = 202
        else:
            outcome = 'Granted'
            ret_code = 200
        
        ret = activityManager.addActivity(user, id_gate, cars['ID'], outcome)
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

        #Eventually check brand
        car = carManager.checkCar(current_user, license_plate)
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
        # photo = request.get_json()['photo']

        if id_gate is None:
            return "Invalid input data", 400
        lst = gateManager.checkSensors()
        lst[0].__str__
        if id_gate not in lst:
            return "Invalid input data", 400
        if name is None:
            return "Invalid input data", 400
        if location is None:
            return "Invalid input data", 400

        gate = gateManager.checkGate(current_user, id_gate)
        if gate == 500:
            return 'Server error', 500
        if gate is not None:
            return 'Gate already exists', 409

        ret = gateManager.addGate(current_user, id_gate, name, location)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return 'Success', 200

    @token_required
    def get(self, current_user):

        id_gate = request.get_json()['id_gate']

        gate = gate.getGate(current_user, id_gate)
        if gate is None:
            return "No Gate found", 404
        if gate == 500:
            return "Server error", 500
        else:
            return jsonify(gate)

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
            if (user['Jtw_refresh'] != token):
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
            
# class UpdateLocation(Resource):
#     @token_required
#     def post(self, current_user):
        
#         if not userManager.checkUser(current_user):
#             return "User not found", 404

#         content = request.get_json()

#         #TODO: insert location checks, return 400 if not OK

#         if not userManager.checkLocation(content):
#             return "Location already exists", 409

#         if userManager.updateLocation(content):
#             return "Success", 200
#         else:
#             return "Internal server error", 500

#TODO: Correct all the paths or the openapi
api.add_resource(ActivityAPI, f'{basePath}/activity')
api.add_resource(CarAPI, f'{basePath}/car')
api.add_resource(GateAPI, f'{basePath}/gate')
api.add_resource(RefreshJWT, f'{basePath}/jwt')
api.add_resource(SigninUser, f'{basePath}/user/signin')
api.add_resource(LoginUser, f'{basePath}/user/login')
api.add_resource(LogoutUser, f'{basePath}/user/logout')
#api.add_resource(UpdateLocation, f'{basePath}/user/location')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
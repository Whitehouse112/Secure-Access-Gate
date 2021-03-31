from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import jwt
import datetime
from gate import GateManager
from user import UserManager, User
from activity import ActivityManager
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'

gate = GateManager()
userManager = UserManager()
activity = ActivityManager()

STATUS = ['granted', 'denied', 'ignored', 'pending', 'reported']

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

class GateAPI(Resource):
    @token_required
    def post(current_user, self):
        content = request.get_json()
        if not gate.checkGate(content):
            return "Invalid input data", 400

        if gate.exists(content):
            return "Gate already exists", 409

        if gate.addGate(content):
            return f"Success + {current_user}", 200
        else:
            return "Internal server error", 500

    @token_required
    def get(current_user, self):
        if not userManager.checkUser(current_user):
            return "Invalid input data", 400

        ret = gate.getGate(current_user)
        if ret != []:
            return ret, 200
        else:
            return "No Gate found", 404

class ActivityAPI(Resource):
    def post(self):
        content = request.get_json()
        if not activity.checkActivity(content):
            return "Invalid input data", 400

        if activity.exists(content):
            return "Activity already exists", 409

        if activity.addActivity(content):
            return "Success", 200
        else:
            return "Internal server error", 500

    @token_required
    def put(current_user, self):
        activityId = request.get_json()['activityId']
        userId = request.get_json()['userId']
        status = request.get_json()['status']

        if activity.checkActivity(userId, activityId):
            return "No Activity found", 404

        if status not in STATUS:
            return "Invalid input data", 400

        if activity.updateActivity(userId, activityId, status):
            return "Internal server error", 500
        else:
            return "Success", 200

    @token_required
    def get(current_user, self):
        if not user.checkUser(current_user):
            return "Invalid input data", 400

        ret = activity.getActivity(current_user)
        if ret != []:
            return ret, 200
        else:
            return "No Gate found", 404

class CreateUser(Resource):
    def post(self):
        content = request.get_json()

        ret = userManager.checkUser(content['email'])
        
        if ret == 500:
            return 'Server error', 500

        if ret is not None:
            return 'User already exists', 409

        hashed_password = generate_password_hash(content['password'], method='sha256')
        #TODO: create the User, and create the new database instance
        #TODO: correct the openAPI, should it return a json object? containing what?
        return 'Success', 200

class LoginUser(Resource):
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return "Invalid input data", 400
        
        user = userManager.getUser(auth.username)

        if not user:
            return "Invalid username/password supplied", 401

        if check_password_hash(user.password, auth.password):
            jwt_refresh = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=30)}, app.config['SECRET_KEY'])   
            jwt_expiry = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
            return jsonify({'jwt_token':jwt_refresh, 'jwt_token_expiry':jwt_expiry})

        return "Invalid username/password supplied", 401

class LogoutUser(Resource):
    @token_required
    def get(current_user, self):
        if not user.checkUser(current_user):
            return "User not found", 404

        if user.logoutUser(current_user):
            return ret, 200
        else:
            return "Internal server error", 500

class UpdateLocation(Resource):
    @token_required
    def post(current_user, self):
        if not userManager.checkUser(current_user):
            return "User not found", 404

        content = request.form

        #TODO: insert location checks, return 400 if not OK

        if not userManager.checkLocation(content):
            return "Location already exists", 409

        if userManager.updateLocation(content):
            return "Success", 200
        else:
            return "Internal server error", 500

class RefreshJWT(Resource):
    def post(self):
        token = request.form['jwt_refresh']

        if not token:
            return "Invalid input data", 400

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
            #TODO: check on database if user has the same refresh token
            if not userManager.checkUser(current_user):
                return "Token is invalid", 401
        except:
            return "Token is invalid", 401
        
        jwt_expiry = jwt.encode({'user':current_user, 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'jwt_token_expiry':jwt_expiry})

#TODO: Correct all the paths or the openapi
api.add_resource(GateAPI, f'{basePath}/gate')
api.add_resource(ActivityAPI, f'{basePath}/activity')
api.add_resource(CreateUser, f'{basePath}/user/signin')
api.add_resource(LoginUser, f'{basePath}/user/login')
api.add_resource(LogoutUser, f'{basePath}/user/logout')
api.add_resource(UpdateLocation, f'{basePath}/user/location')
api.add_resource(RefreshJWT, f'{basePath}/jwt')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
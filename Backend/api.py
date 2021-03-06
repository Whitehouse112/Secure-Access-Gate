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
userManage = UserManager()
activity = ActivityManager()

STATUS = ['granted', 'denied', 'ignored', 'pending', 'reported']


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return "Token is missing", 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            #TODO: correct with actual user db information
            current_user = userManager.getUser(data['user'])
        except:
            return "Token is invalid", 403

        return f(current_user, *args, **kwargs)

    return decorated


class AddGate(Resource):
    @token_required
    def post(self, current_user):
        content = request.get_json()
        if not gate.checkGate(content):
            return "Invalid input data", 400

        if gate.exists(content):
            return "Gate already exists", 409

        if gate.addGate(content):
            return "Success", 200
        else:
            return "Internal server error", 500
      
class CheckGate(Resource):
    def get(self, userId):
        if not user.checkUser(userId):
            return "Invalid input data", 400

        ret = gate.getGate(userId)
        if ret != []:
            return ret, 200
        else:
            return "No Gate found", 404

class UpdateActivity(Resource):
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

    def put(self):
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

class CheckActivity(Resource):
    def get(self, userId):
        if not user.checkUser(userId):
            return "Invalid input data", 400

        ret = activity.getActivity(userId)
        if ret != []:
            return ret, 200
        else:
            return "No Gate found", 404

class CreateUser(Resource):
    def post(self):
        content = request.get_json()

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
            #TODO: setting to be tuned, 24 hours for example
            token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token':token})

        return "Invalid username/password supplied", 401

class LogoutUser(Resource):
    pass

api.add_resource(AddGate, f'{basePath}/gate')
api.add_resource(CheckGate, f'{basePath}/gate/<string:userId>')
api.add_resource(UpdateActivity, f'{basePath}/activity')
api.add_resource(CheckActivity, f'{basePath}/activity/<string:userId>')
api.add_resource(LoginUser, f'{basePath}/login')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
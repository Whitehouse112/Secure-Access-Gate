from flask import Flask, request
from flask_restful import Resource, Api
from gate import GateManager
from user import UserManager
from activity import ActivityManager

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'

gate = GateManager()
user = UserManager()
activity = ActivityManager()
STATUS = ['granted', 'denied', 'ignored', 'pending', 'reported']

class AddGate(Resource):
    def post(self):
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
    pass

class LoginUser(Resource):
    pass

class LogoutUser(Resource):
    pass

api.add_resource(AddGate, f'{basePath}/gate')
api.add_resource(CheckGate, f'{basePath}/gate/<string:userId>')
api.add_resource(UpdateActivity, f'{basePath}/activity')
api.add_resource(CheckActivity, f'{basePath}/activity/<string:userId>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
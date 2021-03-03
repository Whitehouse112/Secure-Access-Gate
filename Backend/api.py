from flask import Flask, request
from flask_restful import Resource, Api
from gate import GateManager

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'

gate = GateManager()

class AddGate(Resource):
    def post(self):
        content = request.get_data()
        if not gate.checkGate(content):
            return "Invalid data", 400

        if not gate.exists(content):
            return "Gate already exists", 409


        if gate.addGate(content):
            return "Success", 200
        else:
            return "Internal server error", 500

        


class CheckGate(Resource):
    pass

class AddActivity(Resource):
    pass

class UpdateActivity(Resource):
    pass

class CheckActivity(Resource):
    pass

class CreateUser(Resource):
    pass

class LoginUser(Resource):
    pass

class LogoutUser(Resource):
    pass

api.add_resource(AddGate, f'{basePath}/gate')
api.add_resource(AddActivity, f'{basePath}/activity')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
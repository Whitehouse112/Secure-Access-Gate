import jwt
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from activityManager import ActivityManager
from anomalyDetection import AnomalyDetection
from carManager import CarManager
from gateManager import GateManager
from userManager import UserManager
from pubsub import PubSub
from storage import Storage
from notification import Notification
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import pubsub

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Secret'
basePath = '/api/v1'
photo_url = "https://storage.googleapis.com/secure-access-photos/"
#TODO: eliminare prima di caricare su cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="files/key.json"

activityManager = ActivityManager()
anomalyDetection = AnomalyDetection()
carManager = CarManager()
gateManager = GateManager()
userManager = UserManager()
storage = Storage()
pubsub = PubSub()
notification = Notification()

STATUS = ['Granted', 'Denied', 'Ignored', 'Pending', 'Reported']
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
        photo = request.get_json()['photo']
        
        if gateManager.checkSensors(id_gate) is None:
            return "Invalid input data", 400
        if license_plate is None or len(license_plate) != 7:
            return "Invalid input data", 400
        if color not in COLOR:
            return "Invalid input data", 400
        if photo is None:
            return "Invalid input data", 400

        user = userManager.checkGate(id_gate)['ID_User']
        if user == 500:
            return 'Internal server error', 500
        if user is None:
            return 'User not found', 404

        id_car = carManager.checkCar(user, license_plate, color)['ID']
        if id_car == 500:
            return 'Internal server error', 500
        if id_car is None:
            return 'Car not found', 404

        gate = gateManager.checkGate(user, id_gate)
        if gate == 500:
            return 'Internal server error', 500
        if gate is None:
            return "Gate not found", 404
        current_location = gate['Location']
        gate_name = gate['Name']

        token = userManager.getUser(user)['FCM_token']
        if token == 500:
            return 'Internal server error', 500
        if token is None:
            return 'Token not found', 404

        date_time = datetime.datetime.now()
        date_time = date_time.strftime("%Y%m%d-%H%M%S")
        photo_name = f"guests_accesses/{id_gate}/{date_time}"

        # Controllo se la macchina è di un utente temporaneo, 
        # nel caso non devo eseguire i controlli di anomalie
        guest = userManager.checkGuest(id_car)
        if guest == 500:
            return "Internal server error", 500
        if guest is not None:
            # Controllo la validità della scadenza dell'autorizzazione
            current_datetime = datetime.datetime.strptime(date_time, '%Y%m%d-%H%M%S')
            deadline = guest['Deadline']
            if deadline < current_datetime:
                #TODO: ritornare solo il messaggio di errore o notificare l'utente
                # per autorizzare eventualmente l'ospite?
                return "Deadline date has expired", 401

            # Carico la foto sul cloud
            ret = storage.upload_image(photo, photo_name)
            if ret == 500:
                return 'Internal server error', 500
            
            # Notifico l'utente sull'accesso da parte dell'ospite
            title = "Nuovo accesso rilevato"
            body = f"L'utente {guest['Nickname']} ha effettuato l'accesso al cancello '{gate_name}'"
            data = {"id_gate":id_gate}
            notification.sendToDevice(token, title, body, data)
            
            ret = activityManager.addGuestActivity(user, id_gate, id_car, 'Granted', photo_url+photo_name)
            return 'Granted', 200

        # Ottengo la lista di attività dell'utente e controllo le
        # anomalie in termini di incongruenze con data e ora
        activities = activityManager.getActivities(user, id_gate)
        if activities == 500:
            return 'Internal server error', 500
        if len(activities) < 5:
            time_anomaly = 0
        else:
            time_anomaly = anomalyDetection.detect_dateTime(activities)

        if time_anomaly == 0:
            # Ottengo la lista delle ultime posizioni dell'utente e controllo le
            # anomalie in termini di incongruenze con l'attuale posizione
            locations = userManager.getLocations(user)
            if locations == 500:
                return 'Internal server error', 500
            if len(locations) < 5:
                location_anomaly = 0
            else:
                location_anomaly = anomalyDetection.detect_locations(locations, gate['Latitude'], gate['Longitude'])
        else:
            location_anomaly = 0

        # Carico l'immagine su cloud storage
        ret = storage.upload_image(photo, photo_name)
        if ret == 500:
            return 'Internal server error', 500

        # Controllo se sono state rilevate o meno delle anomalie
        if time_anomaly >= 1 or location_anomaly == 1:
            outcome = 'Pending'
            ret_code = 202
            
            # Notifico l'utente sullo stato dell'accesso in 'Pending'
            title = "Nuovo accesso rilevato"
            body = f"Tentativo di accesso al cancello '{gate_name}': autorizzare l'accesso?"
            data = {"id_gate":id_gate}
            notification.sendToDevice(token, title, body, data)
        else:
            outcome = 'Granted'
            ret_code = 200
           
        ret = activityManager.addActivity(user, id_gate, id_car, outcome, photo_url+photo_name)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return outcome, ret_code
        
    @token_required
    def put(self, current_user):

        id_gate = request.get_json()['id_gate']
        outcome = request.get_json()['outcome']
        status = 'Pending'

        last_activity = activityManager.getLastActivity(current_user, id_gate, status)
        if last_activity == 500:
            return 'Internal server error', 500
        if last_activity is None:
            return'No activity found', 404

        ret = activityManager.updateActivity(current_user, id_gate, last_activity['Date_Time'], status, outcome)
        if ret == 500:
            return "Internal server error", 500
        
        if outcome == 'Granted':
            pubsub.publishTopic(bytes(id_gate, 'utf-8'))
        if outcome == 'Reported':
            gate = gateManager.checkGate(current_user, id_gate)
            if gate == 500:
                return "Internal server error", 500
            if gate is None:
                return "Invalid input data", 400

            # ex: [Via Ippolito Nievo, 112, 41124 Modena MO, Italy]
            location = gate['Locartion']
            location = location.split(",")
            cap = location[2].split(" ")[0]
            topic = f"{location[0]} {cap}"
            title = "Allerta vicinato"
            body = f"Segnalazione sospetta in {location[0]}"
            notification.sendToTopic(topic, title, body)
        return "Success", 200

    @token_required
    def get(self, current_user):
        
        activities = activityManager.getActivities(current_user)
        if activities == 500:
            return 'Internal server error', 500
        
        guests_activities = activityManager.getGuestsActivities(current_user)
        if guests_activities == 500:
            return 'Internal server error', 500

        return {'activities':activities, 'guests_activities': guests_activities}, 200

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
            return 'Internal server error', 500
        if car is not None:
            return "Car already exists", 409

        ret = carManager.addCar(current_user, license_plate, color, brand)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return 'Success', 200

    @token_required
    def get(self, current_user):
        
        cars = carManager.getCars(current_user)
        if cars == 500:
            return 'Internal server error', 500

        return {'cars':cars}, 200

class UpdateFCM(Resource):
    @token_required
    def post(self, current_user):
        fcm_token = request.get_json()['fcm_token']
        if not fcm_token:
            return "Invalid input data", 400
        
        ret = userManager.updateFCM(current_user, fcm_token)
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
        photo = request.get_json()['photo']

        url_image = ""

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
            return 'Internal server error', 500
        if gate is not None:
            return 'Gate already exists', 409

        if photo != 'null':
            # Se presente, carico l'immagine su cloud storage
            photo_name = f"gates/{current_user}/{id_gate}"
            photo = bytes.fromhex(photo)
            ret = storage.upload_image(photo, photo_name)
            if ret == 500:
                return 'Internal server error', 500
            ret = gateManager.addGate(current_user, id_gate, name, location, latitude, longitude, photo_url+photo_name)
            url_image = photo_url + photo_name
        else:
            ret = pubsub.createTopic(id_gate)
            if ret == 500:
                return 'Internal server error', 500  
            ret = gateManager.addGate(current_user, id_gate, name, location, latitude, longitude, None)
        
        if ret == 500:
            return 'Internal server error', 500
        else:
            if url_image != "":
               return jsonify({'url_image': url_image}), 200
            else: 
                return 'Success', 200

    @token_required
    def get(self, current_user):

        gates = gateManager.getGates(current_user)
        if gates == 500:
            return "Internal server error", 500
        if gates is None:
            return "No Gate found", 404

        return {'gates': gates}, 200

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

class GuestAPI(Resource):
    @token_required
    def post(self, current_user):

        nickname = request.get_json()['nickname']
        dead_line = request.get_json()['dead_line']
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
            return 'Internal server error', 500
        if car is None:
            ret = carManager.addCar(current_user, license_plate, color, brand)
            if ret == 500:
                return 'Internal server error', 500
            car = carManager.checkCar(current_user, license_plate, color)
            if car == 500:
                return 'Internal server error', 500

        id_car = car['ID']
        ret = userManager.addGuest(current_user, id_car, dead_line, nickname)
        if ret == 500:
            return 'Internal server error', 500
        else:
            return 'Success', 200

    @token_required
    def get(self, current_user):

        guests = userManager.getGuests(current_user)
        if guests == 500:
            return "Internal server error", 500
        if guests is None:
            return "No Guests found", 404
        
        return {'guests':guests}, 200

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

class NotificationAPI(Resource):
    @token_required
    def post(self, current_user):

        location = request.get_json()['Location']
        if location is None:
            return "Invalid input data", 400
        
        location = location.replace(" ", "")
        location = location.split(',')
        topic = location[0] + "-" + location[2]
        title = "Segnalazione"
        body = f"Segnalazione utente sospetto nel quartiere {topic}"
        notification.sendToTopic(topic, title, body)

class UserAPI(Resource):
    @token_required
    def get(self, current_user):
        
        user = userManager.getUser(current_user)
        if user == 500:
            return "Internal server error", 500
        if user == []:
            return "User not found", 404 

        return jsonify({'user': user})

class SigninUser(Resource):
    def post(self):
        
        email = request.get_json()['email']
        pwd = request.get_json()['password']
        nickname = request.get_json()['nickname']
        if email is None:
            return "Invalid input data", 400
        if pwd is None:
            return "Invalid input data", 400
        if nickname is None:
            return "Invalid input data", 400

        user = userManager.checkUser(email)
        if user == 500:
            return 'Internal server error', 500
        if user is not None:
            return 'User already exists', 409

        hashed_password = generate_password_hash(pwd, method='sha256') 
        ret = userManager.addUser(email, hashed_password, nickname)
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
            return "Internal server error", 500
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

        altitude = request.get_json()['altitude']
        latitude = request.get_json()['latitude']
        longitude = request.get_json()['longitude']
        if latitude is None:
            return "Invalid input data", 400
        if longitude is None:
            return "Invalid input data", 400

        user = userManager.getUser(current_user)
        if user == 500:
            return "Internal server error", 500
        if user is None:
            return "User not found", 404 

        ret = userManager.updateLocation(current_user, float(latitude), float(longitude))
        if ret == 500:
            return "Internal server error", 500
        else:
            return "Success", 200
            
api.add_resource(ActivityAPI, f'{basePath}/activity')
api.add_resource(CarAPI, f'{basePath}/car')
api.add_resource(UpdateFCM, f'{basePath}/fcm')
api.add_resource(GateAPI, f'{basePath}/gate')
api.add_resource(OpenGateAPI, f'{basePath}/gate/open')
api.add_resource(GuestAPI, f'{basePath}/guest')
api.add_resource(RefreshJWT, f'{basePath}/jwt')
api.add_resource(NotificationAPI, f'{basePath}/notification')
api.add_resource(UserAPI, f'{basePath}/user')
api.add_resource(SigninUser, f'{basePath}/user/signin')
api.add_resource(LoginUser, f'{basePath}/user/login')
api.add_resource(LogoutUser, f'{basePath}/user/logout')
api.add_resource(UpdateLocation, f'{basePath}/user/location')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
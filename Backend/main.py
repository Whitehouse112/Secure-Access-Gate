from flask import Flask
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
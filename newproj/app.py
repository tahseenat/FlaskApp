from flask import Flask, request, jsonify
import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

# Init app
app = Flask(__name__)


# login function
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    payload = {
        'username': username,
        'password': password
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    token = {
        'token': str(jwt_token)
    }
    return token


@app.route('/login', methods=['POST'])
def image_thumbnail():
    token = request.json['token']
    return token


if __name__ == '__main__':
    app.run(debug=True)

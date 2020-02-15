from flask import Flask, request, jsonify
import jwt
import urllib.request
import base64
import cv2
from functools import wraps

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

img_name = "original.jpg"
thumbnail_name = "thumb.jpg"

width = 50
height = 50
dim = (width, height)

# Init app
app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, JWT_SECRET)
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)

    return decorated


# login function
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except:
        return jsonify({'message': 'username/password is missing'})

    if len(username) > 0 and len(password) > 0:
        payload = {
            'username': username,
            'password': password
        }
        header = {
            "alg": JWT_ALGORITHM,
            "typ": "JWT"
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return jsonify({'token': jwt_token.decode('UTF-8')})
    else:
        return jsonify({'message': 'username/password is Invalid'})


@app.route('/image_thumbnail', methods=['POST'])
@token_required
def image_thumbnail():
    try:
        image_url = request.json['image_url']
    except:
        return jsonify({'message': 'Token/image_url is missing'})

    try:
        f = open(img_name, 'wb')
        f.write(urllib.request.urlopen(image_url).read())
        f.close()
    except:
        return jsonify({'message': 'Invalid URL'})

    image_name = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
    thumbnail_image = cv2.resize(image_name, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("thumb.jpg", thumbnail_image)

    string = base64.b64encode(cv2.imencode(thumbnail_name, thumbnail_image)[1]).decode()
    message = {
        'status': 'Success',
        'thumbnail': string
    }
    return message


@app.route('/json_patching', methods=['POST'])
@token_required
def json_patching():
    data = request.json

    return "hello"


if __name__ == '__main__':
    app.run(debug=True)

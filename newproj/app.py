from flask import Flask, request, jsonify
import jwt
import urllib.request
import base64
import cv2
from functools import wraps
import jsonpatch

# specify the secret string you want to encode the json with
JWT_SECRET = 'secret'
# specify the algorithm for encoding
JWT_ALGORITHM = 'HS256'

# name of the original file saved in the dir
img_name = "original.jpg"
# name of the thumbnail file
thumbnail_name = "thumb.jpg"

# specify the dimension of the thumbnail
width = 50
height = 50
dim = (width, height)

# Init app
app = Flask(__name__)


# this function can be used to authorize the request, only valid request will pass
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
#  http://127.0.0.1:5000/login
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


# json thumbnail generator
# http: // 127.0.0.1: 5000 / image_thumbnail?token = secret
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


# json patching
# http: // 127.0.0.1: 5000 / json_patching?token = secret
@app.route('/json_patching', methods=['POST'])
@token_required
def json_patching():
    data = request.json
    patch = jsonpatch.JsonPatch([
        {'op': 'add', 'path': '/foo', 'value': 'bar'},
        {'op': 'add', 'path': '/baz', 'value': [1, 2, 3]},
        {'op': 'remove', 'path': '/baz/1'},
        {'op': 'test', 'path': '/baz', 'value': [1, 3]},
        {'op': 'replace', 'path': '/baz/0', 'value': 42},
        {'op': 'remove', 'path': '/baz/1'},
    ])
    result = patch.apply(data)

    return result


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import jwt
import urllib.request
import base64
import cv2

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

img_name = "original.jpg"
thumbnail_name = "thumb.jpg"

width = 50
height = 50
dim = (width, height)

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
    dict = {
        'token': str(jwt_token)
    }
    return dict


@app.route('/image_thumbnail', methods=['POST'])
def image_thumbnail():
    # token = request.json['token']
    image_url = request.json['image_url']

    f = open(img_name, 'wb')
    f.write(urllib.request.urlopen(image_url).read())
    f.close()
    image_name = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
    thumbnail_image = cv2.resize(image_name, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("thumb.jpg", thumbnail_image)

    string = base64.b64encode(cv2.imencode(thumbnail_name, thumbnail_image)[1]).decode()
    dict = {
        'thumbnail': string
    }
    return dict


@app.route('/json_patching', methods=['POST'])
def json_patching():
    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
